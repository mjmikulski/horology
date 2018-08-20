import unittest
from contextlib import redirect_stdout
from time import sleep
from io import StringIO

from TTT import Timing

class TimedContextTest(unittest.TestCase):
    def test_no_args(self):
        out = StringIO()
        with redirect_stdout(out):
            with Timing():
                sleep(0.15)

            print_str:str = out.getvalue().strip()

        self.assertTrue(print_str.startswith('0.1'))

    def test_interval_property(self):
        with Timing(print_fn=None, unit='ms') as t:
            # should be zero at beginning
            self.assertAlmostEqual(t.interval, 0, delta=0.02)

            # check in meantime
            sleep(0.15)
            self.assertAlmostEqual(t.interval, 0.15, delta=0.02)

            sleep(0.15)

        # check after the context was exited
        self.assertAlmostEqual(t.interval, 0.3, delta=0.02)

        # make sure timing was stopped after the context was exited
        sleep(0.15)
        self.assertAlmostEqual(t.interval, 0.3, delta=0.02)

if __name__ == '__main__':
    unittest.main()