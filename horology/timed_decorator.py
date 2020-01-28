from functools import wraps
from time import perf_counter as counter
from typing import Callable

from horology.tformatter import rescale_time


def timed(f: Callable = None, name=None, *, unit='a', print_fn=print, iterations=1):
    def decorator(_f):
        @wraps(_f)
        def wrapped(*args, **kwargs):
            start = counter()            
            for _ in range(iterations):
                return_value = _f(*args, **kwargs)
            interval = counter() - start
            wrapped.interval = interval
            if print_fn is not None:
                nonlocal name
                if name is None:
                    name = _f.__name__ + ': '
                t, u = rescale_time(interval, unit=unit)
                print_str = f'{name} {t:.2f} {u}'
                if iterations > 1:
                    print_str +=  f" in {iterations} iterations :: Average time per loop = {t/iterations:.2f} {u}"
                print_fn(print_str)
            return return_value
        return wrapped
    if f is None:
        return decorator
    else:        
        return decorator(f)
