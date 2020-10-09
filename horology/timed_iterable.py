from statistics import median, mean, stdev
from time import perf_counter as counter
from typing import Iterable, Callable, Optional

from horology.tformatter import rescale_time


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
        `logger.info`. By default the built-in `print` function is used.

    Attributes
    ----------
    num_iterations: int
        How many iteration were executed.
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
        iteration    1: 12.00 s
        iteration    2: 8.00 s
        iteration    3: 100.00 s

        total 3 iterations in 120.00 s
        min/median/max: 8.00/12.00/100.00 s
        average (std): 40.00 (52.00) s
        ```

    """

    def __init__(self, iterable: Iterable, *,
                 unit='a',
                 iteration_print_fn: Optional[Callable] = print,
                 summary_print_fn: Optional[Callable] = print):

        self.iterable = iterable
        self.unit = unit
        self.iteration_print_fn = iteration_print_fn or (lambda _: None)
        self.summary_print_fn = summary_print_fn or (lambda _: None)

        self.intervals = []
        self._start = None
        self._last = None

    def __iter__(self):
        self._start = counter()
        self.iterable = iter(self.iterable)
        return self

    def __next__(self):
        try:
            now = counter()
            if self._last:
                interval = now - self._last
                self.intervals.append(interval)
                t, u = rescale_time(interval, self.unit)
                self.iteration_print_fn(f"iteration {self.n:4}: {t:.2f} {u}")

            self._last = now

            return next(self.iterable)

        except StopIteration:
            self.print_summary()
            raise StopIteration

    @property
    def num_iterations(self):
        return len(self.intervals)

    @property
    def n(self):
        """ Deprecated """
        return self.num_iterations

    @property
    def total(self):
        return self._last - self._start

    def print_summary(self):
        """ Print statistics of times elapsed in each iteration

        It is called automatically when the iteration ends.

        Use `summary_print_fn` argument in the constructor to control
        if and where the summary is printed.
        """
        # leave an empty line if iterations and summary are printed to
        # the same output
        if self.iteration_print_fn == self.summary_print_fn:
            print_str = "\n"
        else:
            print_str = ""

        if self.n == 0:
            print_str = "no iterations"
        elif self.n == 1:
            t, u = rescale_time(self.intervals[0], unit=self.unit)
            print_str += f"one iteration: {t:.2f} {u}"
        else:
            t_total, u_total = rescale_time(self.total, self.unit)

            t_median, u = rescale_time(median(self.intervals), self.unit)
            t_min, _ = rescale_time(min(self.intervals), u)
            t_mean, _ = rescale_time(mean(self.intervals), u)
            t_max, _ = rescale_time(max(self.intervals), u)
            t_std, _ = rescale_time(stdev(self.intervals), u)

            print_str += f"total {self.n} iterations "
            print_str += f"in {t_total:.2f} {u_total}\n"
            print_str += f"min/median/max: " \
                         f"{t_min:.2f}" \
                         f"/{t_median:.2f}" \
                         f"/{t_max:.2f} {u}\n"
            print_str += f"average (std): " \
                         f"{t_mean:.2f} " \
                         f"({t_std:.2f}) {u}"

        self.summary_print_fn(print_str)
