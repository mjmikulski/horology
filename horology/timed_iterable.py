from statistics import median, mean, stdev
from time import perf_counter as counter
from typing import Iterable, Callable, Optional, List

from horology.tformatter import rescale_time, UnitType


class Timed:
    """ Wrapper to an iterable that measures time of each iteration

    Parameters
    ----------
    iterable: Iterable
        Object that should we wrapped.
    unit: str, optional
        Time unit used to print elapsed time. Possible values:
         ['ns', 'us', 'ms', 's', 'min', 'h', 'd']. Use 'a' or 'auto'
         for automatic time adjustment (default).
    iteration_print_fn: Callable, optional
        Function that is called after each iteration to print time
        of that iteration. Use `None` to disable printing after each
        iteration. You can provide e.g. `logger.debug`. By default
        the built-in `print` function is used.
    summary_print_fn: Callable, optional
        Function that is called to print the summary. Use `None` to
        disable printing the summary. You can provide e.g.
        `logger.info`. By default, the built-in `print` function is used.

    Properties
    ----------
    num_iterations: int
        How many iteration were executed.
    total: float
        Total time elapsed in seconds.

    Example
    -------
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
        ```
    """

    def __init__(
            self,
            iterable: Iterable,
            *,
            unit: UnitType = 'a',
            iteration_print_fn: Optional[Callable] = print,
            summary_print_fn: Optional[Callable] = print
    ) -> None:

        self.iterable = iterable
        self.unit = unit
        self.iteration_print_fn = iteration_print_fn or (lambda _: None)
        self.summary_print_fn = summary_print_fn or (lambda _: None)

        self.intervals: List[float] = []
        self._start: Optional[float] = None
        self._last: Optional[float] = None

    def __iter__(self):
        self._start = counter()
        self.iterable = iter(self.iterable)
        return self

    def __next__(self):
        try:
            now = counter()
            if self._last is not None:
                interval = now - self._last
                self.intervals.append(interval)
                t, u = rescale_time(interval, self.unit)
                self.iteration_print_fn(f'iteration {self.num_iterations:4}: {t:.3g} {u}')

            self._last = now

            return next(self.iterable)

        except StopIteration:
            self.print_summary()
            raise StopIteration

    def __len__(self) -> int:
        return self.iterable.__len__()  # type: ignore

    @property
    def num_iterations(self) -> int:
        return len(self.intervals)

    @property
    def n(self) -> int:
        "Deprecated"
        return self.num_iterations

    @property
    def total(self) -> float:
        try:
            return self._last - self._start  # type: ignore
        except TypeError:
            return 0

    def print_summary(self) -> None:
        """ Print statistics of times elapsed in each iteration

        It is called automatically when the iteration ends.

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

        self.summary_print_fn(print_str)
