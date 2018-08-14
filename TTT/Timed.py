# Copyright (c) 2018 Maciej J. Mikulski

import random
from statistics import median, mean
from time import perf_counter as counter, sleep


class Timed:
    def __init__(self, seq, *, print_fn=print, summary=True, iterations=True):
        self.seq = seq
        self._start = 0
        self._last = 0
        self._intervals = []
        self._first = True
        self._print_fn = print
        self._n = 0
        self._summary = summary
        self._iterations = iterations

    def __iter__(self):
        self.seq = iter(self.seq)
        self._start = counter()
        return self

    def __next__(self):
        try:
            now = counter()
            if not self._first:
                interval = now - self._last
                self._intervals.append(interval)
                if self._iterations:
                    self._print_fn(f"Iteration {self._n:4}: {interval}")
            else:
                self._first = False
            self._last = now

            self._n += 1

            element = next(self.seq)
            return element

        except StopIteration:
            if self._summary:
                self._print_summary()
            raise StopIteration

    def _print_summary(self):
        num_intervals = len(self._intervals)
        print_str = "\n" if self._iterations else ""

        if num_intervals == 0:
            print_str += "No iteration"
        elif num_intervals == 1:
            print_str += f"One iteration: {self._intervals[0]}"
        elif num_intervals == 2:
            print_str += f"Two iterations: {self._intervals[0]} and {self._intervals[1]}"
        else:
            print_str += f"total {num_intervals} iterations in {self._last - self._start}\n"
            print_str += f"min/median/max/average: {min(self._intervals)}/{median(self._intervals)}/{max(self._intervals)}/{mean(self._intervals)}"

        self._print_fn(print_str)


L = range(10)

for x in Timed(L):
    sleep(random.uniform(0, 0.1 * x))
