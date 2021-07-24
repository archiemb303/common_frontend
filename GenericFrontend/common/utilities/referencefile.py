#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import collections
import functools
import os
import pkgutil
import sys
from argparse import _SubParsersAction
from collections import defaultdict
from difflib import get_close_matches
from importlib import import_module
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

import django
from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import (
    BaseCommand, CommandError, CommandParser, handle_default_options,
)
from django.core.management.color import color_style
from django.utils import autoreload
from common.utilities.procedures.procdefinitionvariables.procdefinitionvariables_collection import *
from user.utilities.procedures.procdefinitionvariables.procdefinitionvariables_collection import *
from gymmanagement.utilities.procedures.procdefinitionvariables.procdefinitionvariables_collection import *


def find_commands(management_dir):
    """
    Given a path to a management directory, return a list of all the command
    names that are available.
    """
    command_dir = os.path.join(management_dir, 'commands')
    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]


def load_command_class(app_name, name):
    """
    Given a command name and an application name, return the Command
    class instance. Allow all errors raised by the import process
    (ImportError, AttributeError) to propagate.
    """
    module = import_module('%s.management.commands.%s' % (app_name, name))
    return module.Command()


@functools.lru_cache(maxsize=None)
def get_commands():
    """
    Return a dictionary mapping command names to their callback applications.

    Look for a management.commands package in django.core, and in each
    installed application -- if a commands package exists, register all
    commands in that package.

    Core commands are always included. If a settings module has been
    specified, also include user-defined commands.

    The dictionary is in the format {command_name: app_name}. Key-value
    pairs from this dictionary can then be used in calls to
    load_command_class(app_name, command_name)

    If a specific version of a command must be loaded (e.g., with the
    startapp command), the instantiated module can be placed in the
    dictionary in place of the application name.

    The dictionary is cached on the first call and reused on subsequent
    calls.
    """
    commands = {name: 'django.core' for name in find_commands(__path__[0])}

    if not settings.configured:
        return commands

    for app_config in reversed(list(apps.get_app_configs())):
        path = os.path.join(app_config.path, 'management')
        commands.update({name: app_config.name for name in find_commands(path)})

    return commands


def fetch_command(self, subcommand):
    """
    Try to fetch the given subcommand, printing a message with the
    appropriate command called from the command line (usually
    "django-admin" or "manage.py") if it can't be found.
    """
    # Get commands outside of try block to prevent swallowing exceptions
    commands = get_commands()
    try:
        app_name = commands[subcommand]
    except KeyError:
        if os.environ.get('DJANGO_SETTINGS_MODULE'):
            # If `subcommand` is missing due to misconfigured settings, the
            # following line will retrigger an ImproperlyConfigured exception
            # (get_commands() swallows the original one) so the user is
            # informed about it.
            settings.INSTALLED_APPS
        else:
            sys.stderr.write("No Django settings specified.\n")
        possible_matches = get_close_matches(subcommand, commands)
        sys.stderr.write('Unknown command: %r' % subcommand)
        if possible_matches:
            sys.stderr.write('. Did you mean %s?' % possible_matches[0])
        sys.stderr.write("\nType '%s help' for usage.\n" % self.prog_name)
        sys.exit(1)
    if isinstance(app_name, BaseCommand):
        # If the command is already loaded, use it directly.
        klass = app_name
    else:
        klass = load_command_class(app_name, subcommand)
    return klass

def autocomplete(self):
    """
    Output completion suggestions for BASH.

    The output of this function is passed to BASH's `COMREPLY` variable and
    treated as completion suggestions. `COMREPLY` expects a space
    separated string as the result.

    The `COMP_WORDS` and `COMP_CWORD` BASH environment variables are used
    to get information about the cli input. Please refer to the BASH
    man-page for more information about this variables.

    Subcommand options are saved as pairs. A pair consists of
    the long option string (e.g. '--exclude') and a boolean
    value indicating if the option requires arguments. When printing to
    stdout, an equal sign is appended to options which require arguments.

    Note: If debugging this function, it is recommended to write the debug
    output in a separate file. Otherwise the debug output will be treated
    and formatted as potential completion suggestions.
    """
    # Don't complete if user hasn't sourced bash_completion file.
    if 'DJANGO_AUTO_COMPLETE' not in os.environ:
        return

    cwords = os.environ['COMP_WORDS'].split()[1:]
    cword = int(os.environ['COMP_CWORD'])

    try:
        curr = cwords[cword - 1]
    except IndexError:
        curr = ''

    subcommands = [*get_commands(), 'help']
    options = [('--help', False)]

    # subcommand
    if cword == 1:
        print(' '.join(sorted(filter(lambda x: x.startswith(curr), subcommands))))
    # subcommand options
    # special case: the 'help' subcommand has no options
    elif cwords[0] in subcommands and cwords[0] != 'help':
        subcommand_cls = self.fetch_command(cwords[0])
        # special case: add the names of installed apps to options
        if cwords[0] in ('dumpdata', 'sqlmigrate', 'sqlsequencereset', 'test'):
            try:
                app_configs = apps.get_app_configs()
                # Get the last part of the dotted path as the app name.
                options.extend((app_config.label, 0) for app_config in app_configs)
            except ImportError:
                # Fail silently if DJANGO_SETTINGS_MODULE isn't set. The
                # user will find out once they execute the command.
                pass
        parser = subcommand_cls.create_parser('', cwords[0])
        options.extend(
            (min(s_opt.option_strings), s_opt.nargs != 0)
            for s_opt in parser._actions if s_opt.option_strings
        )
        # filter out previously specified options from available options
        prev_opts = {x.split('=')[0] for x in cwords[1:cword - 1]}
        options = (opt for opt in options if opt[0] not in prev_opts)

        # filter options by current input
        options = sorted((k, v) for k, v in options if k.startswith(curr))
        for opt_label, require_arg in options:
            # append '=' to options which require args
            if require_arg:
                opt_label += '='
            print(opt_label)
    # Exit code of the bash completion function is never passed back to
    # the user, so it's safe to always exit with 0.
    # For more details see #25420.
    sys.exit(0)
