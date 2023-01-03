from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import Mock, patch

from horology import timed


@patch('horology.timed_decorator.counter')
class TestDecorator:

    def test_no_args(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0.12]

        @timed
        def foo():
            pass

        with redirect_stdout(out := StringIO()):
            foo()
            print_str = out.getvalue().strip()

        assert print_str == 'foo: 120 ms'

    def test_with_name_and_unit(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 21]

        @timed(name='Function foo elapsed ', unit='ms')
        def foo():
            pass

        with redirect_stdout(out := StringIO()):
            foo()
            print_str = out.getvalue().strip()

        assert print_str == 'Function foo elapsed 2.1e+04 ms'

    def test_wrapping_transparently(self, _: Mock) -> None:
        @timed(name='bar elapsed: ', unit='auto')
        def bar():
            """Very important function"""

        assert bar.__doc__ == 'Very important function'
        assert bar.__name__ == 'bar'

    def test_interval_property(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 1, 2, 3]

        @timed
        def bar():
            pass

        assert not counter_mock.called

        bar()
        assert bar.interval == 1
        assert counter_mock.call_count == 2

        assert bar.interval == 1
        assert counter_mock.call_count == 2

        bar()
        assert bar.interval == 1
        assert counter_mock.call_count == 4

    def test_usage_without_print(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0.07]

        @timed(print_fn=None)
        def bar():
            pass

        with redirect_stdout(out := StringIO()):
            bar()
            print_str = out.getvalue().strip()

        assert print_str == ''
