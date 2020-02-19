from functools import wraps
from time import perf_counter as counter
from typing import Callable

from horology.tformatter import rescale_time


def timed(f: Callable = None, name=None, *, unit='a', print_fn=print, decimal_precision=2):
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

                nonlocal decimal_precision
                decimal_precision = 2 if not isinstance(decimal_precision, int) else decimal_precision
                    
                print_str = f'{name}{t:.{decimal_precision}f} {u}'
                print_fn(print_str)
                wrapped.timed_float = float(f'{t:.{decimal_precision}f}')

            return return_value
        return wrapped
    if f is None:
        return decorator
    else:        
        return decorator(f)
