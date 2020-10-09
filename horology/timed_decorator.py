from functools import wraps
from time import perf_counter as counter
from typing import Callable

from horology.tformatter import rescale_time


def timed(f: Callable = None, name=None, *, unit='a', print_fn=print):
    """ Decorator that prints time of execution of a function

    Parameters
    ----------
    f: Callable
        The function which execution time should be measured.
    name: str or None, optional
        String that should be printed as the function name. By default
        the f.__name__ proceeded by a colon and space is used, like this:
        ```
        @timed
        def foo():
            pass
        foo() # prints 'foo: 5.12 ms'

        @timed(name='bar elapsed ')
        def bar():
            pass
        bar() # prints 'bar elapsed 2.56 ms'
        ```
    unit: str, optional
        Time unit used to print elapsed time. Possible values:
         ['ns', 'us', 'ms', 's', 'min', 'h', 'd']. Use 'a' or 'auto'
         for automatic time adjustment (default).
    print_fn: Callable or None, optional
        Function that is called to print the time elapsed. Use `None` to
        disable printing anything. You can provide e.g. `logger.info`.
        By default the built-in `print` function is used.

    Returns
    -------
    Decorated function.

    """

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
                print_str = f'{name}{t:.2f} {u}'
                print_fn(print_str)
            return return_value

        return wrapped

    if f is None:
        return decorator
    else:
        return decorator(f)
