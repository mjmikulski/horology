import inspect
from collections.abc import Awaitable, Callable
from functools import wraps
from time import perf_counter as counter
from typing import Any, ParamSpec, Protocol, TypeVar, cast, overload

from horology.tformatter import UnitType, rescale_time

P = ParamSpec('P')
R = TypeVar('R')
R_co = TypeVar('R_co', covariant=True)


class CallableWithInterval(Protocol[P, R_co]):
    """Protocol to represent a callable with interval attribute.

    References
    ----------
    [PEP 612](https://peps.python.org/pep-0612/)
    """
    interval: float
    __name__: str

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R_co: ...


@overload
def timed(f: Callable[P, R]) -> CallableWithInterval[P, R]: ...  # Bare decorator usage


@overload
def timed(
        *,
        name: str | None = None,
        unit: UnitType = 'auto',
        print_fn: Callable[..., Any] | None = print
) -> Callable[[Callable[P, R]], CallableWithInterval[P, R]]: ...  # Decorator with arguments


def timed(
        f: Callable[P, R] | None = None,
        *,
        name: str | None = None,
        unit: UnitType = 'auto',
        print_fn: Callable[..., Any] | None = print
) -> CallableWithInterval[P, R] | Callable[[Callable[P, R]], CallableWithInterval[P, R]]:
    """Decorator that prints time of execution of the decorated function

    Parameters
    ----------
    f: Callable
        The function which execution time should be measured. It can be
        also an async function - then the time until the returned
        coroutine finishes is measured.
    name: str or None, optional
        String that should be printed as the function name. By default,
        the f.__name__ followed by a colon is used. It is separated from
        the time value with a space. See examples below.
    unit: {'auto', 'ns', 'us', 'ms', 's', 'min', 'h', 'd'}
        Time unit used to print elapsed time. Use 'a' or 'auto' for
        automatic time adjustment (default).
    print_fn: Callable or None, optional
        Function that is called to print the time elapsed. Use `None` to
        disable printing anything. You can provide e.g. `logger.info`.
        By default, the built-in `print` function is used.

    If the function raises an exception, the time elapsed is added to
    the exception as a note, so it is shown in the traceback, e.g.
    'horology: foo: 1.02 s (failed)'.

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
        @timed(name='bar elapsed')
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

    Async functions
        ```
        @timed
        async def fetch():
            ...
        await fetch() # prints 'fetch: 1.02 s'
        ```

    """

    def decorator(_f: Callable[P, R]) -> CallableWithInterval[P, R]:
        label = _f.__name__ + ':' if name is None else name

        def report(start: float, exception: Exception | None = None) -> None:
            interval = counter() - start
            timed_f.interval = interval
            t, u = rescale_time(interval, unit=unit)
            print_str = f'{label + " " if label else ""}{t:.3g} {u}'
            if exception is not None:
                print_str += ' (failed)'
                exception.add_note(f'horology: {print_str}')
            if print_fn is not None:
                print_fn(print_str)

        if inspect.iscoroutinefunction(_f):
            coroutine_f = cast(Callable[P, Awaitable[Any]], _f)

            @wraps(_f)
            async def async_wrapped(*args: P.args, **kwargs: P.kwargs) -> Any:
                start = counter()
                try:
                    return_value = await coroutine_f(*args, **kwargs)
                except Exception as e:
                    report(start, e)
                    raise
                report(start)
                return return_value

            wrapped = cast(Callable[P, R], async_wrapped)
        else:
            @wraps(_f)
            def sync_wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
                start = counter()
                try:
                    return_value = _f(*args, **kwargs)
                except Exception as e:
                    report(start, e)
                    raise
                report(start)
                return return_value

            wrapped = sync_wrapped

        timed_f = cast(CallableWithInterval[P, R], wrapped)
        return timed_f

    if f is None:  # used with ()
        return decorator
    else:  # used without ()
        return decorator(f)
