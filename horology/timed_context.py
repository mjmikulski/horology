from time import perf_counter as counter, sleep

from horology.tformatter import rescale_time


class Timing:
    """ Timing context

    # Example
    >>> with Timing('sleeping: ', unit='ms') as t:
    ...    sleep(0.25)
    sleeping: 2... ms
    """

    def __init__(self, name=None, *, unit='a', print_fn=print, decimal_precision=2):
        self.name = name if name else ""
        self.unit = unit
        self._print_fn = print_fn if print_fn else lambda _: None

        self._start = None
        self._interval = None

        self.decimal_precision = decimal_precision 
        if not isinstance(decimal_precision, int):
            self.decimal_precision = 2

    @property 
    def interval(self):
        """ Time elapsed in seconds
        If still in the context, returns time elapsed from the moment of entering to the context.
        If the context has been already left, returns the time spent in the context.
        """
        if self._interval:  # when context exited
            return self._interval
        else:  # when still in context
            return counter() - self._start

    def __enter__(self):
        self._start = counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._interval = self.interval
        t, u = rescale_time(self.interval, self.unit)
        print_str = f"{self.name}{t:.{self.decimal_precision}f} {u}"
        self._print_fn(print_str)


if __name__ == '__main__':
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS)
