# Copyright (c) 2018 Maciej J. Mikulski


from statistics import median, mean
from time import perf_counter as counter

from TTT.tformatter import rescale_time


class Timed:
    def __init__(self, iterable, *, unit='s', print_fn=print, summary=True, iterations=True):
        self.iterable = iterable
        self.unit = unit
        self._print_fn = print_fn if print_fn else lambda _: None
        self._summary = summary
        self._iterations = iterations

        self.intervals = []
        self._n = 0
        self._start = 0
        self._last = 0

    def __iter__(self):
        self._start = counter()
        self.iterable = iter(self.iterable)
        return self

    def __next__(self):
        try:
            now = counter()
            if self._n > 0:
                interval = now - self._last
                self.intervals.append(interval)
                if self._iterations:
                    t, u = rescale_time(interval, self.unit)
                    self._print_fn(f"Iteration {self._n:4}: {t} {u}")

            self._last = now

            element = next(self.iterable)
            self._n += 1
            return element

        except StopIteration:
            if self._summary:
                self._print_summary()
            raise StopIteration

    def _print_summary(self):  # todo: use rescale_time function
        num_intervals = len(self.intervals)
        print_str = "\n" if self._iterations else ""  # leave a empty line if iterations are printed

        if num_intervals == 0:
            print_str += "No iterations"
        elif num_intervals == 1:
            print_str += f"One iteration: {self.intervals[0]}"
        elif num_intervals == 2:
            print_str += f"Two iterations: {self.intervals[0]} and {self.intervals[1]}"
        else:
            print_str += f"total {num_intervals} iterations in {self._last - self._start}\n"
            print_str += f"min/median/max/average: {min(self.intervals)}/{median(self.intervals)}/{max(self.intervals)}/{mean(self.intervals)}"

        self._print_fn(print_str)

#
# import random
# L = range(6)
#
# for x in Timed(L, unit='ms'):
#     sleep(random.uniform(0, 0.1 * x))
