"""
Multiprocess engine
=======================
Module to execute multiprocessing over given data.
"""

import time
import concurrent.futures


def function_wrapper():
    # If the process is nested then put all the functional calls within this function (thus the name *_wrapper).
    pass


if __name__ == "__main__":
    PLACEHOLDER_LIST = []  # list of iterables. These become the input for function_wrapper

    with concurrent.futures.ProcessPoolExecutor() as executor:
        start_time = time.perf_counter()
        result = list(executor.map(function_wrapper, PLACEHOLDER_LIST))
        finish_time = time.perf_counter()
    print(f"Program finished in {finish_time - start_time} seconds")
    print(result)
