import pytest

from horology.tformatter import rescale_time


class TestTformatter:

    def test_no_rescaling(self) -> None:
        t, u = rescale_time(6, unit='s')
        assert t == 6 and u == 's'

    def test_simple_format(self) -> None:
        t, u = rescale_time(6, unit='ms')
        assert t == 6000 and u == 'ms'

        t, u = rescale_time(6, unit='min')
        assert t == 0.1 and u == 'min'

    def test_auto_format(self) -> None:
        t, u = rescale_time(6, unit='a')
        assert t == 6 and u == 's'

        t, u = rescale_time(0.006, unit='auto')
        assert t == 6 and u == 'ms'

        t, u = rescale_time(6000, unit='AUTO')  # type: ignore
        assert t == 100 and u == 'min'

    def test_wrong_unit(self) -> None:
        with pytest.raises(ValueError, match='Unknown unit: lustrum. Use one of the following:'):
            rescale_time(0.5, 'lustrum')  # type: ignore
