import unittest
from contextlib import redirect_stdout
from io import StringIO
from time import sleep

from TTT import Timed


class TimedIterableTest(unittest.TestCase):
    def test_no_iter(self):
        out = StringIO()
        with redirect_stdout(out):
            for _ in Timed([]):
                pass
            print_str: str = out.getvalue().strip()
        self.assertEqual(print_str, 'no iterations')

    def test_one_iteration(self):
        out = StringIO()
        with redirect_stdout(out):
            for _ in Timed([1], unit='s'):
                sleep(0.15)
            print_str: str = out.getvalue().strip()

        lines = print_str.split('\n')

        self.assertTrue(lines[0].startswith('iteration    1: 0.1'))
        self.assertTrue(lines[0].endswith('s'))

        self.assertEqual(lines[1], '')

        self.assertTrue(lines[2].startswith('one iteration: 0.1'))
        self.assertTrue(lines[2].endswith('s'))

    def test_summary(self):
        out = StringIO()
        with redirect_stdout(out):
            for k in Timed(range(1, 6)):
                sleep(0.1 * k)
            print_str: str = out.getvalue().strip()

        lines = print_str.split('\n')

        self.assertTrue(lines[-3].startswith('total 5 iterations in 1.5'))
        self.assertTrue(lines[-2].endswith('s'))

        self.assertTrue(lines[-2].startswith('min/median/max:'))
        self.assertTrue(lines[-2].endswith('ms'))

        self.assertTrue(lines[-1].startswith('average (std): 3'))
        self.assertTrue(lines[-1].endswith('ms'))

    def test_no_print(self):
        out = StringIO()
        with redirect_stdout(out):
            T = Timed(['cat', 'dog', 'parrot'], iteration_print_fn=None, summary_print_fn=None)
            for a in T:
                sleep(0.15)
                print(a)
            print_str: str = out.getvalue().strip()

        lines = print_str.split('\n')
        self.assertListEqual(lines, ['cat', 'dog', 'parrot'])
        self.assertAlmostEqual(T.total, 0.45, delta=0.05)


if __name__ == '__main__':
    unittest.main()
