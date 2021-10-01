from functools import wraps
from time import perf_counter as counter
from typing import Callable

from horology.tformatter import rescale_time


def timed(f: Callable = None, name=None, *, unit='auto', print_fn=print):
    """ Decorator that prints time of execution of a function

    Parameters
    ----------
    f: Callable
        The function which execution time should be measured.
    name: str or None, optional
        String that should be printed as the function name. By default
        the f.__name__ proceeded by a colon and space is used. See
        examples below.
    unit: {'auto', 'ns', 'us', 'ms', 's', 'min', 'h', 'd'}
        Time unit used to print elapsed time. Use 'a' or 'auto' for
        automatic time adjustment (default).
    print_fn: Callable or None, optional
        Function that is called to print the time elapsed. Use `None` to
        disable printing anything. You can provide e.g. `logger.info`.
        By default the built-in `print` function is used.

    Attributes
    ----------
    interval: float
        Time elapsed by the function in seconds. Can be used to get the
        time programmatically after the execution of f.

    Returns
    -------
    Decorated function.

    Examples
    --------
    Basic usage
        ```
        @timed
        def foo():
            ...
        foo() # prints 'foo: 5.12 ms'
        ```

    Change default name
        ```
        @timed(name='bar elapsed ')
        def bar():
            ...
        bar() # prints 'bar elapsed 2.56 ms'
        ```

    Change default units
        ```
        @timed(unit='ns')
        def baz():
            ...
        baz() # prints 'baz: 32768.15 ns'
        ```

    Suppress printing and use the attribute `interval` to get the time
    elapsed
        ```
        @timed(print_fn=None)
        def qux():
            ...
        qux() # prints nothing
        print(qux.interval)
        ```
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
