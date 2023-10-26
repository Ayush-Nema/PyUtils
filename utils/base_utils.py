"""
Base utils
=============
Curation of general purpose utility functions
"""

import json
import logging
import logging.config as log_config
import os

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


def read_configs(_config_path="configs.json"):
    """
    Simple module to read the configuration file and distribute the vals among all functions.

    :param _config_path: path of the configuration file (`.json`)
    :type _config_path: str
    :return: reads the configurations
    :rtype: dict
    """
    return read_json(_config_path)


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
