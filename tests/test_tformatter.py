import unittest

from horology.tformatter import rescale_time


class TformatterTest(unittest.TestCase):

    def test_simple_format(self):
        t, u = rescale_time(6, unit='s')
        self.assertEqual((t, u), (6, 's'))

        t, u = rescale_time(6, unit='ms')
        self.assertEqual((t, u), (6000, 'ms'))

        t, u = rescale_time(6, unit='min')
        self.assertEqual((t, u), (0.1, 'min'))

    def test_auto_format(self):
        t, u = rescale_time(6, unit='a')
        self.assertEqual((t, u), (6, 's'))

        t, u = rescale_time(0.006, unit='auto')
        self.assertEqual((t, u), (6, 'ms'))

        t, u = rescale_time(6000, unit='AUTO')
        self.assertEqual((t, u), (100, 'min'))

    def test_value_error(self):
        self.assertRaises(ValueError, rescale_time, 0.5, unit='lustrum')


if __name__ == '__main__':
    unittest.main()
