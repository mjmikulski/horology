from __future__ import annotations

from time import perf_counter as counter
from types import TracebackType
from typing import Any, Callable, Literal, Type

from horology.tformatter import UnitType, rescale_time


class Timing:
    """Context manager that measures time elapsed with the context

    Use `interval` property to get the time elapsed.

    Parameters
    ----------
    name: str, optional
        Message that should be printed before the time value, e.g.:
        'Doing x: '
    unit: str, optional
        Time unit used to print elapsed time. Possible values are:
         ['ns', 'us', 'ms', 's', 'min', 'h', 'd']. Use 'a' or 'auto'
         for automatic time adjustment (default).
    print_fn: Callable or None, optional
        Function that is called to print the time elapsed in the
        context. Use `None` to disable printing anything. You can
        provide e.g. `logger.info`. By default, the built-in `print`
        function is used.

    Example
    -------
    Basic usage
        ```
        from horology import Timing
        with Timing(name='Important calculations: '):
            do_a_lot()
        ```
        Possible result:
        ```
        Important calculations: 12.4 s
        ```
    """

    def __init__(
            self,
            name: str | None = None,
            *,
            unit: UnitType = 'auto',
            print_fn: Callable[..., Any] | None = print
    ) -> None:
        self.name = name if name else ""
        self.unit = unit
        self._print_fn = print_fn

        self._start: float | None = None
        self._interval: float | None = None

    @property
    def interval(self) -> float:
        """Time elapsed in seconds

        If still in the context, returns time elapsed from the moment
        of entering to the context. If the context has been already
        left, returns the total time spent in the context.

        """
        if self._start is None:
            raise RuntimeError('`interval` can be accessed only inside the '
                               'context or after exiting it.')

        if self._interval:  # when the context exited
            return self._interval
        else:  # when still in the context
            return counter() - self._start

    def __enter__(self) -> Timing:
        self._start = counter()
        return self

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None,
    ) -> Literal[False]:
        self._interval = self.interval
        t, u = rescale_time(self.interval, self.unit)
        if self._print_fn is not None:
            print_str = f'{self.name}{t:.3g} {u}'
            if exc_type is not None:
                print_str += ' (failed)'
            self._print_fn(print_str)
        return False
