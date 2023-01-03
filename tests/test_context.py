from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import Mock, patch

from horology import Timing


@patch('horology.timed_context.counter')
class TestContext:
    def test_no_args(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0.12]

        with redirect_stdout(out := StringIO()):
            with Timing():
                pass
            print_str = out.getvalue().strip()

        assert print_str == '120 ms'

    def test_if_independent_to_absolute_time_values(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [100.05, 100.17]

        with redirect_stdout(out := StringIO()):
            with Timing():
                pass
            print_str = out.getvalue().strip()

        assert print_str == '120 ms'

    def test_with_name_and_unit(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0.12]

        with redirect_stdout(out := StringIO()):
            with Timing(name='Preprocessing: ', unit='s'):
                pass
            print_str = out.getvalue().strip()

        assert print_str == 'Preprocessing: 0.12 s'

    def test_interval_property(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0.12, 0.24, 0.36, 0.48]  # last value never used
        from horology import Timing

        with Timing(print_fn=None, unit='ms') as t:
            # should increase
            assert t.interval == 0.12

            # should increase
            assert t.interval == 0.24

        # counter should not be called after exiting the context
        assert counter_mock.call_count == 4

        # check after the context was exited
        assert t.interval == 0.36

        # make sure timing was stopped after the context was exited
        assert t.interval == 0.36

        # check again that counter was not called after context has been exited
        assert counter_mock.call_count == 4
