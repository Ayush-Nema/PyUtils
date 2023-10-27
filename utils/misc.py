"""
Miscellaneous util functions
=============================
Miscellaneous utility functions
"""

import logging
import time
from functools import wraps

# Initialising the logger
LOGGER = logging.getLogger(__name__)


def run_time(func):
    """
    Computes the run-time of the calling function.

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
