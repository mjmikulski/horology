from functools import wraps
from time import perf_counter as counter
from typing import Callable

from TTT.tformatter import rescale_time


def timed(f: Callable = None, name=None, *, unit='s', print_fn=print):
    def decorator(_f):
        @wraps(_f)
        def wrapped(*args, **kwargs):
            start = counter()
            return_value = _f(*args, **kwargs)
            interval = counter() - start
            wrapped.interval = interval

            if print_fn is not None:
                nonlocal name
                if name is None:
                    name = _f.__name__ + ': '
                t, u = rescale_time(interval, unit=unit)
                print_str = f'{name}{t:.3f} {u}'
                print_fn(print_str)
            return return_value

        return wrapped

    if f is None:
        return decorator
    else:
        return decorator(f)
