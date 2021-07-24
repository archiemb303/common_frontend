#!/usr/bin/env python
"""Django's command-line utility for Procedures Operation."""
import os
import sys
import re
import collections
import logging
import subprocess

# Get an instance of a logger
logger = logging.getLogger("genericfrontend_1.0")


def execute(generateprocpath, procs_variablespath, generateprocs_filepath,  argv):
    """
    Given the command-line arguments, figure out which subcommand is being
    run, create a parser appropriate to that command, and run it.
    """
    try:
        subcommand = generateprocpath + argv[1]
        for (procsvariables, outputpath) in zip(procs_variablespath, generateprocs_filepath):
            subprocess.call(f"python {subcommand}.py --filename {procsvariables} --output_path {outputpath}",
                            shell=True)
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Issues happened while calling generate procss "
                                                                  f"and procedure files. Encountered Exception: {ex}",
                                                                  None]))
        return output_json


def get_duplicates(generateprocs_filepath):
    """
    Get all the duplicate procedure files.
    """
    try:
        procfiles_list = []
        for filepaths in generateprocs_filepath:
            procfiles_list.extend(os.listdir(filepaths))
        duplicateprocslist = [item for item, count in collections.Counter(procfiles_list).items() if count > 1]
        return duplicateprocslist
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Issues happened while fetchin duplicate procedure "
                                                                  f"files. Encountered Exception: {ex}", None]))
    return output_json


def get_filecontent(filename):
    """Fetch the contents of file having procedure definitions stored as strings in variable. """
    try:
        with open(filename, 'r') as f:
            return f.read().splitlines()
    except Exception as ex:
        output_json = dict(zip(['Message', 'Payload'],
                               [f'Encountered exception in reading contents of stored procedure variables : {ex} ',
                                None]))
        return output_json


def add_importprocdefvarpath(arg ):
    """Add Proc definition variables path for new folder  to import file proc defnition variable path."""
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        importprocdefpath = 'common/utilities/procedures/importfile_procdefinitionvariables.py'
        sys.path.insert(0, os.path.join(BASE_DIR, f'{importprocdefpath}'))
        for path in sys.path:
            if 'importfile_procdefinitionvariables.py' in path:
                arg = arg.split('/')[0]
                added_importprocdefpath = f'from {arg}.utilities.procedures.procdefinitionvariables.procdefinitionvariables_collection import *'
                with open(path, 'a') as f:
                    f.write(added_importprocdefpath)
                fileread = get_filecontent(str(path))
                for item in fileread:
                    if added_importprocdefpath not in item:
                        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                                  f"Issues in adding Import file Path",
                                                                                  None]))
                        return output_json
                match1 = re.findall(r"'Status': 'Failure'", str(fileread))
                if match1:
                    return fileread
                return
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Issues happened while creating import file."
                                                                  f" Encountered Exception: {ex}", None]))
        return output_json


def main():
    try:
        # Set the OS environment Django Settings module to sp_manage
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genericfrontend.sp_manage')
        pathlist, list1, list2 = [], [], []
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        procdefinitionvariables_path = 'utilities/procedures/procdefinitionvariables'
        procdefinitiongeneratedfiles_path = 'utilities/procedures/procdefinitions_generatedfiles'
        appfolderlist = [
            'common',
            'gymmanagement',
            'user',
            'demo',
            'multimedia',
            'tests'
            ]
        sp_path_list = [procdefinitionvariables_path, procdefinitiongeneratedfiles_path]
        for appfolder in appfolderlist:
            for sp_path in sp_path_list:
                filepath = f'{appfolder}/{sp_path}'
                pathlist.append(filepath)
        for path in pathlist:
            sys.path.insert(0, os.path.join(BASE_DIR, f'{path}'))
        generateprocs_filepath, procs_variablespath = [], []
        for procfile_path in sys.path:
            if 'procdefinitions_generatedfiles' in procfile_path:
                # Create dirctory path, if not present
                if not os.path.isdir(procfile_path):
                    os.makedirs(procfile_path)
                generateprocs_filepath.append(procfile_path)
        for procvar_path in sys.path:
            if 'procdefinitionvariables' in procvar_path:
                if not os.path.isdir(procvar_path):
                    os.mkdir(procvar_path)
                    # Add Proc definition variables path for new folder  to import file proc defnition variable path.
                    add_importprocdefvarpath(filepath)
                    with open(os.path.join(procvar_path, 'procdefinitionvariables_collection.py'), 'w') as fp:
                        pass
                filepath = procvar_path + '/' + 'procdefinitionvariables_collection.py'
                procs_variablespath.append(filepath)

        for path in generateprocs_filepath:
            if 'common' in path:
                generateprocpath = path.replace('procdefinitions_generatedfiles', '')
        # Call get_duplicates function to get the duplicate procs across all folders
        print('Duplicate Procedures are:', get_duplicates(generateprocs_filepath))
        # Call this function to call python subcommand
        execute(generateprocpath, procs_variablespath, generateprocs_filepath, sys.argv)
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Issues happened while creating procedures "
                                                                  f"and procedure files. Encountered Exception: {ex}",
                                                                  None]))
        return output_json


# Entry point for create procdeures utility
if __name__ == '__main__':
    main()
