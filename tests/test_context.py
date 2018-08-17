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





if __name__ == '__main__':
    unittest.main()