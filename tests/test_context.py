from contextlib import redirect_stdout
from io import StringIO
from typing import Any
from unittest.mock import Mock, patch

import pytest

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

    def test_exception_handling_within_context(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0.5]
        exception_raised = False

        with redirect_stdout(out := StringIO()):
            try:
                with Timing():
                    raise ValueError('Test Exception')
            except ValueError:
                exception_raised = True
            print_str = out.getvalue().strip()

        assert exception_raised
        assert print_str == '500 ms (failed)'

    def test_custom_print_function(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0.12]

        def custom_print(*args: Any, **kwargs: Any) -> None:
            print('Custom print function')

        with redirect_stdout(out := StringIO()):
            with Timing(print_fn=custom_print):
                pass
            print_str = out.getvalue().strip()

        assert print_str == 'Custom print function'

    def test_no_printing_when_print_fn_is_none(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0.12]

        with redirect_stdout(out := StringIO()):
            with Timing(print_fn=None):
                pass
            print_str = out.getvalue().strip()

        assert print_str == ''

    def test_error_when_accessing_interval_outside_context(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0.12]
        timing_instance = Timing()

        # Accessing interval before context should raise an error
        with pytest.raises(RuntimeError):
            _ = timing_instance.interval

        # Now use the context normally
        with timing_instance:
            pass

        # Accessing interval after context should not raise an error
        _ = timing_instance.interval
