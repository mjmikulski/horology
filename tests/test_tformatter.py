import unittest

from horology.tformatter import auto_unit, rescale_time


class TformatterTest(unittest.TestCase):
    def test_auto_unit(self):
        self.assertEqual(auto_unit(0.5 * 10 ** -6), 'ns')
        self.assertEqual(auto_unit(2 * 10 ** -6), 'us')
        self.assertEqual(auto_unit(0.5), 'ms')
        self.assertEqual(auto_unit(5), 's')
        self.assertEqual(auto_unit(2000), 'min')

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


if __name__ == '__main__':
    unittest.main()
