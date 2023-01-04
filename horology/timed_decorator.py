from functools import wraps
from time import perf_counter as counter
from typing import Any, Callable, Optional, Protocol, TypeVar, overload

from horology.tformatter import UnitType, rescale_time

F = TypeVar('F', bound=Callable)


class CallableWithInterval(Protocol[F]):
    """
    When support for python version 3.9 and 3.9 is dropped, this should
    be refactored with typing.ParamSpec

    References
    ----------
    [PEP 612](https://peps.python.org/pep-0612/)
    """
    interval: float
    __call__: F
    __name__: str


@overload
def timed(f: F) -> CallableWithInterval[F]: ...  # Bare decorator usage


@overload
def timed(
        *,
        name: Optional[str] = None,
        unit: UnitType = 'auto',
        print_fn: Optional[Callable[..., Any]] = print
) -> Callable[[F], CallableWithInterval[F]]: ...  # Decorator with arguments


def timed(
        f: Optional[Callable] = None,
        *,
        name: Optional[str] = None,
        unit: UnitType = 'auto',
        print_fn: Optional[Callable[..., Any]] = print):
    """Decorator that prints time of execution of the decorated function

    Parameters
    ----------
    f: Callable
        The function which execution time should be measured.
    name: str or None, optional
        String that should be printed as the function name. By default,
        the f.__name__ proceeded by a colon and space is used. See
        examples below.
    unit: {'auto', 'ns', 'us', 'ms', 's', 'min', 'h', 'd'}
        Time unit used to print elapsed time. Use 'a' or 'auto' for
        automatic time adjustment (default).
    print_fn: Callable or None, optional
        Function that is called to print the time elapsed. Use `None` to
        disable printing anything. You can provide e.g. `logger.info`.
        By default, the built-in `print` function is used.

    Attributes
    ----------
    interval: float
        Time elapsed by the function in seconds. Can be used to get the
        time programmatically after the execution of f.

    Returns
    -------
    Callable
        Decorated function `f`.

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
        baz() # prints 'baz: 3.28e+04 ns'
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
                print_str = f'{name}{t:.3g} {u}'
                print_fn(print_str)

            return return_value

        return wrapped

    if f is None:  # used with ()
        return decorator
    else:  # used without ()
        return decorator(f)
