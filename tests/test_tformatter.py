import re

import pytest

from horology.tformatter import UnitType, rescale_time, UNITS


class TestTformatter:

    def test_no_rescaling(self) -> None:
        t, u = rescale_time(6, unit='s')
        assert t == 6 and u == 's'

    def test_simple_format(self) -> None:
        t, u = rescale_time(6, unit='ms')
        assert t == 6000 and u == 'ms'

        t, u = rescale_time(6, unit='min')
        assert t == 0.1 and u == 'min'

    @pytest.mark.parametrize('unit', ['ns', 'us', 'ms', 's', 'min', 'h', 'd'])
    @pytest.mark.parametrize('time_interval', [0.002, 2, 2000])
    def test_unit_is_kept(self, unit: UnitType, time_interval: float) -> None:
        _, u = rescale_time(time_interval, unit=unit)
        assert u == unit

    def test_auto_format(self) -> None:
        t, u = rescale_time(6, unit='a')
        assert t == 6 and u == 's'

        t, u = rescale_time(0.006, unit='auto')
        assert t == 6 and u == 'ms'

        t, u = rescale_time(6000, unit='AUTO')  # type: ignore
        assert t == 100 and u == 'min'

    def test_wrong_unit(self) -> None:
        matching_msg = "Unknown unit: lustrum. Use one of the following: " \
                       "['ns', 'us', 'ms', 's', 'min', 'h', 'd'] or 'auto'"
        with pytest.raises(ValueError, match=re.escape(matching_msg)):
            rescale_time(0.5, 'lustrum')  # type: ignore

    def test_units_order(self) -> None:
        limit = 0.0
        for u in UNITS:
            assert u.limit > limit
            limit = u.limit
