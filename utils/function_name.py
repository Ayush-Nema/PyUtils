"""
Get function name
===================
Getting the function name from inside the function itself
"""
import inspect


def utility_func(a, b):
    print(f"Triggered [{inspect.currentframe().f_code.co_name}] with i/p args: {locals()}")
    return a + b


if __name__ == '__main__':
    _ = utility_func(1, 2)
    # >> Triggered [utility_func] with i/p args: {'a': 1, 'b': 2}

