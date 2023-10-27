"""
Basic utility functions
==========================
The storehouse of basic utility functions which are intended to be used project wide.
"""

import argparse
import json
import logging
import logging.config as log_config
import os
import shutil
import subprocess
import time
from functools import wraps
from glob import glob
from pathlib import Path

from dotenv import dotenv_values, load_dotenv

# Initialising the logger
LOGGER = logging.getLogger(__name__)


def init_cmd_args(args):
    """
    Initialize command line argument parser

    :param args: The list of arguments
    :type args: list
    :return: An initialized argument parser
    :rtype: :class:`argparse.ArgumentParser`
    """

    # Create an argument parser instance
    parser = argparse.ArgumentParser()

    # Add the required/mandatory arguments
    required_args = parser.add_argument_group("required arguments")
    required_args.add_argument("-i", "--input_fp", type=str, required=True, help="File path of the input file")
    required_args.add_argument("-e", "--export_fp", type=str, required=True,
                               help="Path where the output files will be exported")

    # Add the optional arguments
    optional_args = parser.add_argument_group("optional arguments")
    optional_args.add_argument("-l", "--logger_fp", type=int, required=False,
                               help="Filepath of the logging.json file")

    return parser.parse_args(args)


def set_env_vars(env_fp: str):
    """
    Loads the `.env` file containing all the environment variables  and loads them to memory.

    :param env_fp: file path of `.env` file
    :type env_fp: str
    :return: all environment variables with their respective keys
    :rtype: dict
    """

    if not load_dotenv(env_fp):
        raise ValueError(f"No environment vars present in {env_fp} file.")

    e_vars = dict(dotenv_values(env_fp))
    LOGGER.debug(f"Environment variables set are: \n {list(e_vars.keys())}")
    return e_vars


def read_configs(_config_path="configs.json"):
    """
    Simple module to read the configuration file and distribute the vals among all functions.

    :param _config_path: path of the configuration file (`.json`)
    :type _config_path: str
    :return: reads the configurations
    :rtype: dict
    """
    return read_json(_config_path)


def config_logger(log_config_fp):
    """
    Config the logging framework
    :param log_config_fp: The path to the logging framework's configuration file
    :type log_config_fp: str
    :return: Nothing
    :rtype: None
    :raises FileNotFoundError: If the file cannot be found at the given path
    :raises TypeError: If the log_config_fp is not a string
    """
    if not issubclass(type(log_config_fp), str):
        raise TypeError("Logging framework configuration file path has to be a string")

    if not os.path.exists(log_config_fp):
        raise FileNotFoundError("Cannot find the logging framework configuration file at the given path")

    with open(log_config_fp, "r") as log_config_file:
        log_conf = json.load(fp=log_config_file)
    log_config.dictConfig(log_conf)
    LOGGER.info("Logging framework initialised!")


class checkIfExists:
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
    Extract the filename from given path
    :param file_path: path for the intended file
    :type file_path: str
    :return: name of file
    :rtype: str
    """
    return Path(file_path).stem


def run_time(func):
    """
    Computes the run-time of the calling function
    :param func: function
    :return: Nothing
    """

    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        time_elapsed = end_time - start_time
        LOGGER.info(f"Finished {func.__name__!r}{args} {kwargs} in {time_elapsed:.4f} secs")
        return value

    return wrapper_timer


def count_call(func):
    """
    Counts the number of times a function has been called.
    :param func: function
    :return: Nothing
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        result = func(*args, **kwargs)
        print(f'{func.__name__} has been called {wrapper.count} times')
        return result

    wrapper.count = 0
    return wrapper


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
    if checkIfExists.verify_dir(dir_name):
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


def check_nans_in_df(df, col_name=None):
    """
    Checks for NaNs in pandas dataframe object.

    :param df: dataframe in which to inspect for NaNs
    :type df: <class 'pandas.core.frame.DataFrame'>
    :param col_name: specific column(s) in `df` to check for NaNs.
    :type: str or list
    :returns: Returns `True` if NaNs are found, `False` otherwise. And count of NaNs. (if NaNs present, how much)
    :rtype: tuple
    """
    if col_name:
        return df[col_name].isnull().values.any(), df[col_name].isnull().sum()
    else:
        return df.isnull().values.any(), df.isnull().sum()


def merge_dicts(dict1, dict2):
    """
    Merge 2 dictionaries containing the results for Level-1 and Level-2 category.

    :param dict1: 1st dictionary
    :type dict1: dict
    :param dict2: 2nd dictionary
    :type dict2: dict
    :return: aggregated dictionary containing the key:value pair from both individual dicts
    :rtype: dict
    :raise: raises `ValueError` is one or more keys are present in the input dictionaries.
    """

    common_keys = set(dict1.keys()) & set(dict2.keys())
    if common_keys:
        raise ValueError(f"Both dictionaries have overlapping keys: {common_keys}")
    return {**dict1, **dict2}
