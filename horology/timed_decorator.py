from functools import wraps
from time import perf_counter as counter
from typing import Any, Callable, ParamSpec, Protocol, overload

from horology.tformatter import UnitType, rescale_time

P = ParamSpec('P')


class CallableWithInterval(Protocol[P]):
    """Protocol to represent a callable with interval attribute.

    References
    ----------
    [PEP 612](https://peps.python.org/pep-0612/)
    """
    interval: float
    __call__: Callable[P, Any]
    __name__: str


@overload
def timed(f: Callable[P, Any]) -> CallableWithInterval[P]: ...  # Bare decorator usage


@overload
def timed(
        *,
        name: str | None = None,
        unit: UnitType = 'auto',
        print_fn: Callable[..., Any] | None = print
) -> Callable[[Callable[P, Any]], CallableWithInterval[P]]: ...  # Decorator with arguments


def timed(
        f: Callable[P, Any] | None = None,
        *,
        name: str | None = None,
        unit: UnitType = 'auto',
        print_fn: Callable[..., Any] | None = print):
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
            exception = None
            try:
                return_value = _f(*args, **kwargs)
            except Exception as e:
                exception = e
            finally:
                interval = counter() - start
                wrapped.interval = interval

            if print_fn is not None:
                nonlocal name
                name = _f.__name__ + ': ' if name is None else name
                t, u = rescale_time(interval, unit=unit)
                print_str = f'{name}{t:.3g} {u}'
                if exception is not None:
                    print_str += ' (failed)'
                print_fn(print_str)

            if exception is not None:
                raise exception

            return return_value

        return wrapped

    if f is None:  # used with ()
        return decorator
    else:  # used without ()
        return decorator(f)
