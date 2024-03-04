"""
Files and directories
==========================
The storehouse for functions for performing operations with files and directories.
"""

import json
import logging
import os
import shutil
import subprocess
from glob import glob
from pathlib import Path
import pandas as pd

# Initialising the logger
LOGGER = logging.getLogger(__name__)


def read_json(json_path):
    """
    Reads and parses `json` files

    :param json_path: file path of the `json` file
    :type json_path: str
    :return: parsed `json` content
    :rtype: dict
    """
    with open(json_path, "r") as fp:
        json_data = json.load(fp)
    return json_data


class CheckIfExists:
    @staticmethod
    def verify_file(file_path: str):
        """
        Check whether the file exists.

        :param file_path: the file path for the target file
        :type file_path: str
        :return: Returns `True` if file exists, `False` otherwise.
        :rtype: bool
        """
        return os.path.isfile(file_path)

    @staticmethod
    def verify_dir(dir_path: str):
        """
        Check whether the directory exists.

        :param dir_path: the directory path for the target directory
        :type dir_path: str
        :return: Returns `True` if directory exists, `False` otherwise.
        :rtype: bool
        """
        return os.path.isdir(dir_path)


def filename_wo_extn(file_path):
    """
    Extract the filename from given path.

    :param file_path: path for the intended file
    :type file_path: str
    :return: name of file
    :rtype: str
    """
    return Path(file_path).stem


def dir_teardown(dir_name):
    """
    Purge clean an entire directory w/o deleting the directory itself (also removes nested dirs, if found).
    Ref: https://stackoverflow.com/questions/185936/how-to-delete-the-contents-of-a-folder

    :param dir_name: directory which needs to be cleaned.
    :type dir_name: str
    :return: nothing
    :rtype: None
    """
    for file_path in glob(f"{dir_name}/*"):
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            LOGGER.error(f'Failed to delete {file_path}. Reason: {e}.')


class purge_data:
    def __init__(self, direc_path: str):
        self.direc_path = direc_path + "/*"
        self.base_str = "Do you wish to continue? \n" \
                        "Press 'Y' for Yes, else press any key to terminate."

    def purge_directory(self):
        all_content = glob(self.direc_path)
        print(f"All {len(all_content)} files will be deleted.")

        act = input(f"You are going to empty complete data directory. \n"
                    f"This will delete everything and this action is irreversible. \n{self.base_str}")

        if act == 'Y':
            print("Commencing purge operation...")
            self._delete_core(all_content)
            print("All files deleted!")
        else:
            print("Skipping data deletion.")

    def delete_specific(self, f_extn: str):
        # f_extn can be either `.wav` or `.json` (with a leading period (.))
        accepted_extns = ['.wav', '.json']
        if f_extn not in accepted_extns:
            raise TypeError(f"Accepted file extensions are {accepted_extns}. Provided: {f_extn}.")

        all_files_of_this_kind = glob(self.direc_path + f_extn)
        print(f"Total {len(all_files_of_this_kind)} found with [{f_extn}] extension and will be deleted!")

        act = input(f"You are about the delete all [{f_extn}] files from Label Studio media directory. \n"
                    f"This action is irreversible. \n{self.base_str}")

        if act == 'Y':
            self._delete_core(all_files_of_this_kind)
            print(f"All {f_extn} files erased for media directory")
        else:
            print("Skipped data deletion.")

    @staticmethod
    def _delete_core(f_list: list):
        """
        Central module for data deletion. Actual file removal operation takes place here.

        :param f_list: list of all files to be removed
        :type f_list: list
        """
        for f in f_list:
            os.remove(f)

    def deletion_validation(self):
        # Stores the value of initial and final states of media directory.
        # Reports the number of files found for deletion and deleted after operation.
        # Perform base calculation: final count = (initial count - eligible files for deletion). Tallies both sides.
        # Send success or fail message to caller function
        pass



def validate_dir(dir_name: str):
    """
    Validate and cross-verify that intermediate export directories are present, if not create them.
    Checks write permissions (read and write). If r/w permissions are not present then adds them.

    :param dir_name: name of directory to verify for existence and permissions
    :type dir_name: str
    :return: nothing
    :rtype: None
    """
    if CheckIfExists.verify_dir(dir_name):
        LOGGER.debug(f"{dir_name} identified, skipping new creation.")
        if not os.access(dir_name, os.X_OK | os.W_OK):
            # ref: https://www.tutorialspoint.com/How-to-change-the-permission-of-a-directory-using-Python
            # ref: https://www.pluralsight.com/blog/it-ops/linux-file-permissions
            subprocess.call(['chmod', '+rwx', dir_name])
            LOGGER.warning(f"{dir_name} found w/o read & write permissions. Changed the permissions.")
    else:
        # create the dirs with r/w permissions
        # ref: https://stackoverflow.com/questions/47618490/python-create-a-directory-with-777-permissions
        os.makedirs(dir_name, mode=0o777)
        LOGGER.info(f"{dir_name} not found. Created with essential permissions.")


def validate_file_extn(filepath, desired_extn):
    """
    Checks the file extension. If incorrect extension (type) is detected, then raises the TypeError exception.

    :param filepath: path of the file to validate
    :type filepath: str
    :param desired_extn: desired extension for the file mentioned in `filepath` argument
    :type desired_extn: str
    :return: Nothing
    :rtype: None
    :raises: `TypeError` if extension mismatch is identified
    """
    if not filepath.endswith(desired_extn):
        raise TypeError(f"File type should be [{desired_extn}] got [.{filepath.split('.')[-1]}] instead.")


def export_to_csv(func):
    """
    A wrapper for exporting the dataframe as CSV file, given the export path and file name.

    Usage:  
    @export_to_csv
    def create_dataframe():
        data = {'Name': ['John', 'Anna', 'Peter', 'Linda'],
                'Age': [25, 30, 35, 40],
                'City': ['New York', 'Paris', 'London', 'Tokyo']}
        df = pd.DataFrame(data)
        
        # Add export path and filename to the DataFrame metadata
        df._metadata = {'export_path': 'exports', 'export_filename': 'output.csv'}
        
        return df
    """
    
    def wrapper(*args, **kwargs):
        # Call the original function to get the DataFrame
        df = func(*args, **kwargs)
        # Get the export path and filename from the function
        export_path = df._metadata.get('export_path', None)
        export_filename = df._metadata.get('export_filename', None)
        if export_path and export_filename:
            file_path = f"{export_path}/{export_filename}"
            df.to_csv(file_path, index=False)
            print(f"DataFrame exported to {file_path}")
        
        else:
            print("Export path or filename is missing in the DataFrame metadata.")
        return df
    return wrapper
