from statistics import median, mean, stdev
from time import perf_counter as counter
from typing import Iterable

from horology.tformatter import rescale_time


class Timed:
    def __init__(self, iterable: Iterable, *, unit='a', iteration_print_fn=print, summary_print_fn=print, decimal_precision=2):
        self.iterable = iterable
        self.unit = unit
        self.iteration_print_fn = iteration_print_fn if iteration_print_fn else lambda _: None
        self.summary_print_fn = summary_print_fn if summary_print_fn else lambda _: None

        self.intervals = []
        self._start = None
        self._last = None

        self.dp = 2 if not isinstance(decimal_precision, int) else decimal_precision

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
                self.iteration_print_fn(f"iteration {self.n:4}: {t:.{self.dp}f} {u}")

            self._last = now

            return next(self.iterable)

        except StopIteration:
            self.print_summary()
            raise StopIteration

    @property
    def n(self):
        return len(self.intervals)

    @property
    def total(self):
        return float(f'{self._last - self._start:.{self.dp}f}')

    def print_summary(self):
        # leave an empty line if iterations and summary are printed to the same output.
        print_str = "\n" if self.iteration_print_fn == self.summary_print_fn else ""

        if self.n == 0:
            print_str = "no iterations"
        elif self.n == 1:
            t, u = rescale_time(self.intervals[0], unit=self.unit)
            print_str += f"one iteration: {t:.{self.dp}f} {u}"
        else:
            t_total, u_total = rescale_time(self.total, self.unit)

            t_median, u = rescale_time(median(self.intervals), self.unit)
            t_min, _ = rescale_time(min(self.intervals), u)
            t_mean, _ = rescale_time(mean(self.intervals), u)
            t_max, _ = rescale_time(max(self.intervals), u)
            t_std, _ = rescale_time(stdev(self.intervals), u)

            print_str += f"total {self.n} iterations in {t_total:.{self.dp}f} {u_total}\n"
            print_str += f"min/median/max: " \
                         f"{t_min:.{self.dp}f}" \
                         f"/{t_median:.{self.dp}f}" \
                         f"/{t_max:.{self.dp}f} {u}\n"
            print_str += f"average (std): " \
                         f"{t_mean:.{self.dp}f} " \
                         f"({t_std:.{self.dp}f}) {u}"

        self.summary_print_fn(print_str)
