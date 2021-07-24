#!/usr/bin/env python
"""Django's command-line utility for Procedures Operation."""
import os
import sys
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
        input_path = []
        for input in procs_variablespath:
            input_path.append(input.replace('procdefinitionvariables_collection.py', ''))
            # input_path.append(input.replace('tests.py',''))###############################vandana###################
        subprocess.call(f"python {subcommand}.py --filename {procs_variablespath[0]} --input_path {input_path[0]} "
                            f"--output_path {generateprocs_filepath[0]} --query_inputparams {argv[2]}", shell=True)
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


def main():
    # Set the OS environment Django Settings module to sp_manage
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genericfrontend.sp_test_manage')
        pathlist, list1, list2 = [], [], []
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        procdefinitionvariables_path = 'utilities/procedures/procdefinitionvariables'
        procdefinitiongeneratedfiles_path = 'utilities/procedures/procdefinitions_generatedfiles'
        appfolderlist = [
            'testprocs'

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
                if not os.path.isdir(procfile_path):
                    os.makedirs(procfile_path)
                generateprocs_filepath.append(procfile_path)
        for procvar_path in sys.path:
            if 'procdefinitionvariables' in procvar_path:
                # Create dirctory path is not present
                if not os.path.isdir(procvar_path):
                    os.mkdir(procvar_path)
                    with open(os.path.join(procvar_path, 'procdefinitionvariables_collection.py'), 'w') as fp:
                        pass
                filepath = procvar_path + '/' + 'procdefinitionvariables_collection.py'
                procs_variablespath.append(filepath)
        for path in generateprocs_filepath:
            if 'testprocs' in path:
                generateprocpath = path.replace('procdefinitions_generatedfiles', '')
        # Call this function to call python subcommand
        execute(generateprocpath, procs_variablespath, generateprocs_filepath, sys.argv)
    except Exception as ex:
        output_json = dict(zip(['Status', 'Message', 'Payload'], ['Failure',
                                                                  f"Issues happened while creating procedures "
                                                                  f"and procedure files. Encountered Exception: {ex}",
                                                                  None]))
        return output_json


# Entry point for test procdeure utility
if __name__ == '__main__':
    main()
