"""
Miscellaneous util functions
=============================
Miscellaneous utility functions
"""
import json
import filecmp
import hashlib
import logging
import time
import difflib
from functools import wraps

from deepdiff import DeepDiff

from utils.files_and_dirs import read_json

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


class CompareTwoJSONs:
    """
    A class to compare two JSON objects, generate hashes, and identify the differences.
    """
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2

    def naive_compare(self):
        """
        A basic comparison to view whether the files are same or not.
        This is pretty generic and also for variety of file types (not restricted only for JSONs)
        """
        # shallow comparison
        result = filecmp.cmp(self.file1, self.file2)
        LOGGER.debug(result)
        # deep comparison
        result = filecmp.cmp(self.file1, self.file2, shallow=False)
        LOGGER.debug(result)

    def generate_hash(self):
        """
        Generate the hash of JSON content. The encryption algorithm for generating the hash can be changed easily.
        Here `md5` encryption is used.
        To check other encryption types, check out: https://docs.python.org/3/library/hashlib.html#constructors,

        Ref:
        # Apply MD5 hashing: https://debugpointer.com/python/create-md5-hash-of-a-file-in-python
        # Primer about hashing algos: https://kinsta.com/blog/python-hashing/

        :return: hashes for both file contents
        :rtype: tuple[str]
        """

        f1_data, f2_data = read_json(self.file1), read_json(self.file2)

        # Convert dictionaries to JSON strings and then encode as bytes
        f1_data_bytes = json.dumps(f1_data, sort_keys=True).encode('utf-8')
        f2_data_bytes = json.dumps(f2_data, sort_keys=True).encode('utf-8')

        f1_data_md5hash = hashlib.md5(f1_data_bytes).hexdigest()
        f2_data_md5hash = hashlib.md5(f2_data_bytes).hexdigest()
        LOGGER.debug(f"Hash for file #1: {f1_data_md5hash} \nHash for file #2: {f2_data_md5hash}")

        return f1_data_md5hash, f2_data_md5hash

    def hash_compare(self):
        """
        Compare the files based on the hash generated. The type of hash generated can be changed programmatically in
        `generate_hash` method (i.e. hashlib.sha128, hashlib.sha256 etc.).

        :return: None
        :rtype: None
        """

        f1_hash, f2_hash = self.generate_hash()

        if f1_hash == f2_hash:
            LOGGER.info("Both the files are same")
        else:
            LOGGER.warning("Files are different")

    @staticmethod
    def view_json_diffs(file1, file2):
        """
        Comparing two JSONs and reports the differences.
        Uses `deepdiff` library [external] for identifying and reporting the differences.
        Ref: https://zepworks.com/deepdiff/current/

        :param file1: filepath of the 1st JSON file
        :type file1: str
        :param file2: filepath of the 2nd JSON file
        :type file2: str
        :rtype: None
        :rtype: None
        """
        # Reading the files
        json_data1 = read_json(file1)
        json_data2 = read_json(file2)

        # Use DeepDiff to find differences
        diff = DeepDiff(json_data1, json_data2)

        if not diff:
            LOGGER.info("JSON files are identical.")
        else:
            LOGGER.warning(f"Differences found: {diff}")

    @staticmethod
    def view_json_diffs_native(file1, file2):
        """
        Performs same functions as `view_json_diffs` but only difference is it uses native library `difflib` for
        finding the differences.
        Even though the output is descriptive, it is not very helpful when there are multiple diffs. Also,
        o/p might not look great with loggers, thus downgrading to classic print statement.
        Ref: https://stackoverflow.com/questions/19120489/compare-two-files-report-difference-in-python

        :param file1: filepath of the 1st JSON file
        :type file1: str
        :param file2: filepath of the 2nd JSON file
        :type file2: str
        :rtype: None
        :rtype: None
        """

        # Reading the files
        json_data1 = read_json(file1)
        json_data2 = read_json(file2)

        # Splitting the file by new line (using ',' here for delimiting)
        lines1 = json.dumps(json_data1).split(",")
        lines2 = json.dumps(json_data2).split(",")

        for line in difflib.unified_diff(lines1, lines2, fromfile='file1', tofile='file2', lineterm=''):
            print(line)
