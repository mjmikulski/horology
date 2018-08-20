import unittest

from TTT.tformatter import auto_unit, format


class TformatterTest(unittest.TestCase):
    def test_auto_unit(self):
        self.assertEqual(auto_unit(0.5 * 10 ** -6), 'ns')
        self.assertEqual(auto_unit(2 * 10 ** -6), 'us')
        self.assertEqual(auto_unit(0.5), 'ms')
        self.assertEqual(auto_unit(5), 's')
        self.assertEqual(auto_unit(2000), 'min')

    def test_simple_format(self):
        t, u = format(6, unit='s')
        self.assertEqual((t, u), (6, 's'))

        t, u = format(6, unit='ms')
        self.assertEqual((t, u), (6000, 'ms'))

        t, u = format(6, unit='min')
        self.assertEqual((t, u), (0.1, 'min'))

    def test_auto_format(self):
        t, u = format(6, unit='a')
        self.assertEqual((t, u), (6, 's'))

        t, u = format(0.006, unit='auto')
        self.assertEqual((t, u), (6, 'ms'))

        t, u = format(6000, unit='AUTO')
        self.assertEqual((t, u), (100, 'min'))


if __name__ == '__main__':
    unittest.main()
