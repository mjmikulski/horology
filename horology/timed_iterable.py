from __future__ import annotations

from collections.abc import AsyncIterable, AsyncIterator, Callable, Iterable, Iterator
from statistics import mean, median, stdev
from time import perf_counter as counter
from typing import Any, Generic, Self, TypeVar, cast
from warnings import warn

from horology.tformatter import UnitType, rescale_time

T = TypeVar('T')

SPARKS = '▁▂▃▄▅▆▇█'


def draw_sparkline(values: list[float], width: int = 50) -> str:
    """Draw values as a sparkline, scaled from zero to the maximum

    If there are more values than `width`, consecutive values are
    averaged, so the sparkline is not longer than `width`.

    Examples
    --------
    >>> draw_sparkline([1, 2, 4, 8])
    '▂▃▅█'

    """
    if len(values) > width:
        n = len(values)
        values = [mean(values[i * n // width:(i + 1) * n // width])
                  for i in range(width)]

    highest = max(values)
    if highest <= 0:
        return SPARKS[0] * len(values)
    return ''.join(SPARKS[min(int(v / highest * len(SPARKS)), len(SPARKS) - 1)]
                   for v in values)


class Timed(Generic[T]):
    """ Wrapper to an iterable that measures time of each iteration

    Parameters
    ----------
    iterable: Iterable or AsyncIterable
        Object that should be wrapped. Use `async for` to iterate over
        an async iterable.
    unit: str, optional
        Time unit used to print elapsed time. Possible values:
         ['ns', 'us', 'ms', 's', 'min', 'h', 'd']. Use 'a' or 'auto'
         for automatic time adjustment (default).
    iteration_print_fn: Callable, optional
        Function that is called after each iteration to print time
        of that iteration. Use `None` to disable printing after each
        iteration. You can provide e.g. `logger.debug`. By default,
        the built-in `print` function is used.
    summary_print_fn: Callable, optional
        Function that is called to print the summary. Use `None` to
        disable printing the summary. You can provide e.g.
        `logger.info`. By default, the built-in `print` function is used.
    sparkline: bool, optional
        Whether to draw times of all iterations as a sparkline in the
        summary, e.g. `▃█▆▆▆`. It is shown only if there were at least
        2 iterations. By default, True.

    Attributes
    ----------
    num_iterations: int
        How many iterations were executed.
    total: float
        Total time elapsed in seconds.

    Examples
    --------
    Basic usage
        ```
        from horology import Timed
        animals = ['cat', 'dog', 'crocodile']
        for x in Timed(animals):
            feed(x)
        ```

        Possible result:
        ```
        iteration    1: 12.0 s
        iteration    2: 8.00 s
        iteration    3: 100 s

        total 3 iterations in 120 s
        min/median/max: 8.00/12.0/100 s
        average (std): 40.0 (52.0) s
        ▁▁█
        ```

    Async iterables
        ```
        async for page in Timed(fetch_pages()):
            process(page)
        ```
    """

    def __init__(
            self,
            iterable: Iterable[T] | AsyncIterable[T],
            *,
            unit: UnitType = 'a',
            iteration_print_fn: Callable[..., Any] | None = print,
            summary_print_fn: Callable[..., Any] | None = print,
            sparkline: bool = True
    ) -> None:

        self.iterable = iterable
        self.unit: UnitType = unit
        self.iteration_print_fn = iteration_print_fn or (lambda _: None)
        self.summary_print_fn = summary_print_fn or (lambda _: None)
        self.sparkline = sparkline

        self.intervals: list[float] = []
        self._start: float | None = None
        self._last: float | None = None
        self._iterator: Iterator[T]
        self._async_iterator: AsyncIterator[T]

    def __iter__(self) -> Self:
        self._restart()
        self._iterator = iter(cast(Iterable[T], self.iterable))
        return self

    def __next__(self) -> T:
        try:
            self._tick()
            return next(self._iterator)

        except StopIteration:
            self.print_summary()
            raise StopIteration

    def __aiter__(self) -> Self:
        self._restart()
        self._async_iterator = aiter(cast(AsyncIterable[T], self.iterable))
        return self

    async def __anext__(self) -> T:
        try:
            self._tick()
            return await anext(self._async_iterator)

        except StopAsyncIteration:
            self.print_summary()
            raise

    def _restart(self) -> None:
        self.intervals = []
        self._last = None
        self._start = counter()

    def _tick(self) -> None:
        now = counter()
        if self._last is not None:
            interval = now - self._last
            self.intervals.append(interval)
            t, u = rescale_time(interval, self.unit)
            self.iteration_print_fn(f'iteration {self.num_iterations:4}: {t:.3g} {u}')

        self._last = now

    @property
    def num_iterations(self) -> int:
        return len(self.intervals)

    @property
    def n(self) -> int:
        """Deprecated, use `num_iterations` instead"""
        warn('`n` is deprecated and will be removed in horology 2.0, '
             'use `num_iterations` instead', DeprecationWarning, stacklevel=2)
        return self.num_iterations

    @property
    def total(self) -> float:
        try:
            return self._last - self._start  # type: ignore
        except TypeError:
            return 0

    def print_summary(self) -> None:
        """ Print statistics of times elapsed in each iteration

        It is called automatically when the iteration over the iterable
        finishes.

        Use `summary_print_fn` argument in the constructor to control
        if and where the summary is printed.

        """
        # Leave an empty line if iterations and summary are printed to
        # the same output.
        if self.iteration_print_fn == self.summary_print_fn:
            print_str = '\n'
        else:
            print_str = ''

        if self.num_iterations == 0:
            print_str = 'no iterations'
        elif self.num_iterations == 1:
            t, u = rescale_time(self.intervals[0], unit=self.unit)
            print_str += f'one iteration: {t:.3g} {u}'
        else:
            t_total, u_total = rescale_time(self.total, self.unit)

            t_median, u = rescale_time(median(self.intervals), self.unit)
            # For clarity, all values are shown using the same unit.
            t_min, _ = rescale_time(min(self.intervals), u)
            t_mean, _ = rescale_time(mean(self.intervals), u)
            t_max, _ = rescale_time(max(self.intervals), u)
            t_std, _ = rescale_time(stdev(self.intervals), u)

            print_str += f'total {self.num_iterations} iterations '
            print_str += f'in {t_total:.3g} {u_total}\n'
            print_str += f'min/median/max: ' \
                         f'{t_min:.3g}' \
                         f'/{t_median:.3g}' \
                         f'/{t_max:.3g} {u}\n'
            print_str += f'average (std): ' \
                         f'{t_mean:.3g} ' \
                         f'({t_std:.3g}) {u}'
            if self.sparkline:
                print_str += f'\n{draw_sparkline(self.intervals)}'

        self.summary_print_fn(print_str)
