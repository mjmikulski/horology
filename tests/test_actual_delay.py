from contextlib import redirect_stdout
from io import StringIO
from time import sleep

import pytest

from horology import Timed, Timing, timed

@pytest.mark.flaky(reruns=5)
class TestWithSleep:
    def test_context(self):
        with redirect_stdout(out := StringIO()):
            with Timing():
                sleep(0.11)
            print_str = out.getvalue().strip()

        assert print_str.startswith('1')
        assert print_str.endswith('ms')

    def test_decorator(self):
        @timed
        def foo():
            sleep(0.11)

        with redirect_stdout(out := StringIO()):
            foo()
            print_str = out.getvalue().strip()

        assert print_str.startswith('foo: 1')
        assert print_str.endswith('ms')

    def test_iterable(self):
        with redirect_stdout(out := StringIO()):
            for _ in Timed(range(1)):
                sleep(0.11)
            print_str = out.getvalue().strip()

        assert print_str.startswith('iteration    1: 1')
        assert print_str.endswith('ms')
