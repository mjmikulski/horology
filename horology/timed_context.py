from __future__ import annotations

from time import perf_counter as counter
from types import TracebackType
from typing import Optional, Callable, Any, Type, Literal

from horology.tformatter import rescale_time, UnitType


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
            name: Optional[str] = None,
            *,
            unit: UnitType = 'auto',
            print_fn: Optional[Callable[..., Any]] = print
    ) -> None:
        self.name = name if name else ""
        self.unit = unit
        self._print_fn = print_fn if print_fn else lambda _: None

        self._start: Optional[float] = None
        self._interval: Optional[float] = None

    @property
    def interval(self) -> float:
        """Time elapsed in seconds

        If still in the context, returns time elapsed from the moment
        of entering to the context. If the context has been already
        left, returns the total time spent in the context.

        """
        if self._start is None:
            raise RuntimeError('`interval` can be invoked only inside a '
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
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType],
    ) -> Literal[False]:
        self._interval = self.interval
        t, u = rescale_time(self.interval, self.unit)
        print_str = f"{self.name}{t:.3g} {u}"
        self._print_fn(print_str)  # type: ignore
        return False
