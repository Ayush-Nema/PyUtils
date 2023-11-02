"""
Utilities for new project setup
=================================
Storage of functions that are kind-of mandatory for setting up a new project.
"""

import argparse
import json
import logging
import logging.config as log_config
import os

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

    # Better way
    # _ = load_dotenv(find_dotenv())  # OR load_dotenv(env_fp)
    # Output ex for usage: openai.api_key = os.environ['OPENAI_API_KEY']
    return e_vars


def read_configs(_config_path="configs.json"):
    """
    Simple module to read the configuration file and distribute the vals among all functions.

    :param _config_path: path of the configuration file (`.json`)
    :type _config_path: str
    :return: reads the configurations
    :rtype: dict
    """
    with open(_config_path) as fp:
        configs = json.load(fp)
    return configs


def config_logger(log_config_fp):
    """
    Config the logging framework.

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
