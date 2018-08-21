# Copyright (c) 2018 Maciej J. Mikulski


from statistics import median, mean
from time import perf_counter as counter
from typing import Iterable

from TTT.tformatter import rescale_time


class Timed:
    def __init__(self, iterable: Iterable, *, unit='s', iteration_print_fn=print, summary_print_fn=print):
        self.iterable = iterable
        self.unit = unit
        self.iteration_print_fn = iteration_print_fn if iteration_print_fn else lambda _: None
        self.summary_print_fn = summary_print_fn if summary_print_fn else lambda _: None

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
                self.iteration_print_fn(f"iteration {self.n:4}: {t:.3f} {u}")

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
        return self._last - self._start

    def print_summary(self):  # todo: use rescale_time function
        # leave an empty line if iterations and summary are printed to the same output
        print_str = "\n" if self.iteration_print_fn == self.summary_print_fn else ""  

        if self.n == 0:
            print_str = "no iterations"
        elif self.n == 1:
            t, u = rescale_time(self.intervals[0], unit=self.unit)
            print_str += f"one iteration: {t:.3f} {u}"
        else:
            print_str += f"total {self.n} iterations in {self.total:.3f}\n"
            print_str += f"min/median/max/average: {min(self.intervals):.3f}/{median(self.intervals):.3f}/{max(self.intervals):.3f}/{mean(self.intervals):.3f}"

        self.summary_print_fn(print_str)
