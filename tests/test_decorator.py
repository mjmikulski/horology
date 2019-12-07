import unittest
from contextlib import redirect_stdout
from io import StringIO
from time import sleep

from TTT import timed


class TimedDecoratorTest(unittest.TestCase):
    def test_no_args(self):
        # Define a decorated function:
        @timed
        def foo():
            sleep(0.15)

        out = StringIO()
        with redirect_stdout(out):
            # Call decorated function
            foo()

            print_str: str = out.getvalue().strip()

        self.assertTrue(print_str.startswith('foo: 1'))
        self.assertTrue(print_str.endswith('ms'))

    def test_with_name_and_unit(self):
        # Define a decorated function:
        @timed(name='Function foo elapsed ', unit='ms')
        def foo():
            sleep(1.15)

        out = StringIO()
        with redirect_stdout(out):
            # Call decorated function
            foo()

            print_str: str = out.getvalue().strip()

        self.assertTrue(print_str.startswith('Function foo elapsed 11'))
        self.assertTrue(print_str.endswith(' ms'))

    def test_wrapping(self):
        # Define a decorated function:
        @timed(name='bar elapsed: ', unit='auto')
        def bar():
            """Very important function"""
            pass

        # Call decorated function
        bar()

        # bar is transparently wrapped
        self.assertEqual(bar.__doc__, 'Very important function')
        self.assertEqual(bar.__name__, 'bar')

    def test_interval_property(self):
        # Define a decorated function:
        @timed
        def bar(x):
            sleep(x)

        bar(0.15)
        t = bar.interval
        self.assertAlmostEqual(t, 0.15, delta=0.02)

        bar(0.2)
        t = bar.interval
        self.assertAlmostEqual(t, 0.2, delta=0.02)

    def test_usage_without_print(self):
        # Define a decorated function:
        @timed(print_fn=None)
        def bar():
            sleep(0.15)

        # Call decorated function
        bar()
        t = bar.interval

        self.assertAlmostEqual(t, 0.15, delta=0.02)

if __name__ == '__main__':
    unittest.main()