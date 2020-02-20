import unittest
from contextlib import redirect_stdout
from io import StringIO
from time import sleep

from horology import Timing


class TimedContextTest(unittest.TestCase):
    def test_no_args(self):
        out = StringIO()
        with redirect_stdout(out):
            with Timing():
                sleep(0.15)

            print_str: str = out.getvalue().strip()

        self.assertTrue(print_str.startswith('1'))
        self.assertTrue(print_str.endswith('ms'))

    def test_with_name_and_unit(self):
        out = StringIO()
        with redirect_stdout(out):
            with Timing(name='Preprocessing: ', unit='ms'):
                sleep(0.15)

            print_str: str = out.getvalue().strip()

        self.assertTrue(print_str.startswith('Preprocessing: 1'))
        self.assertTrue(print_str.endswith('ms'))

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

    def test_decimal_precision(self):
        with Timing(print_fn=None, unit='ms', decimal_precision=4) as t:
            # should be zero at beginning
            self.assertAlmostEqual(t.interval, 0, delta=0.04)

            # check in meantime
            sleep(0.15)
            self.assertAlmostEqual(t.interval, 0.15, delta=0.04)

            sleep(0.15)
            

        # check after the context was exited
        self.assertAlmostEqual(t.interval, 0.3, delta=0.04)

        # make sure timing was stopped after the context was exited
        sleep(0.15)
        self.assertAlmostEqual(t.interval, 0.3, delta=0.04)

        # Check decimal precision is correct
        self.assertEqual(t.timed_float, round(t.timed_float, 4))
        

    def test_no_decimal_precision(self):
        with Timing(print_fn=None, unit='ms', decimal_precision=None) as t:
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

        # Check decimal precision is correct
        self.assertEqual(t.timed_float, round(t.timed_float, 2))
        
if __name__ == '__main__':
    unittest.main()
