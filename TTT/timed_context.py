from time import perf_counter as counter, sleep

from TTT.tformatter import format


class Timing:
    def __init__(self, name=None, *, unit='s', print_fn=print):
        self.name = name if name else ""
        self.unit = unit
        self._print_fn = print_fn if print_fn else lambda _: None

        self.interval = 0  # todo: make it property
        self._start = 0

    def __enter__(self):
        self._start = counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.interval = counter() - self._start
        t, u = format(self.interval, self.unit)
        print_str = f"{self.name}{t} {u}"
        self._print_fn(print_str)



# with Timing('sleeping: ', unit='ns') as t:
#     sleep(0.2)
#
# print(t.interval)