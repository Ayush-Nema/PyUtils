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
