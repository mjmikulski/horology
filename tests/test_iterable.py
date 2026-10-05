import asyncio
from collections.abc import AsyncIterator
from contextlib import redirect_stdout
from io import StringIO
from typing import assert_type
from unittest.mock import Mock, patch

import pytest

from horology import Timed


@patch('horology.timed_iterable.counter')
class TestTimedIterable:

    def test_no_iter(self, counter_mock: Mock) -> None:
        with redirect_stdout(out := StringIO()):
            for _ in Timed([]):
                pass
            print_str = out.getvalue().strip()

        assert print_str == 'no iterations'
        assert counter_mock.call_count == 2

    def test_one_iteration(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0.01, 1.01]

        with redirect_stdout(out := StringIO()):
            for _ in Timed([1]):
                pass
            lines = out.getvalue().strip().split('\n')

        assert lines[0] == 'iteration    1: 1 s'
        assert lines[1] == ''
        assert lines[2] == 'one iteration: 1 s'

    def test_summary(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [-0.01, 0, 0.5, 2, 3, 4, 5, 6]

        with redirect_stdout(out := StringIO()):
            for _ in Timed(range(5)):
                pass
            lines = out.getvalue().strip().split('\n')

        assert lines[-4] == ''
        assert lines[-3] == 'total 5 iterations in 5.01 s'
        assert lines[-2] == 'min/median/max: 0.5/1/1.5 s'
        assert lines[-1] == 'average (std): 1 (0.354) s'

        assert counter_mock.call_count == 7

    def test_summary_time_rescaling_s(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0, 0.001, 0.002, 0.004]

        with redirect_stdout(out := StringIO()):
            for _ in Timed(range(3), unit='s'):
                pass
            lines = out.getvalue().strip().split('\n')

        assert lines[-3] == 'total 3 iterations in 0.004 s'
        assert lines[-2] == 'min/median/max: 0.001/0.001/0.002 s'
        assert lines[-1] == 'average (std): 0.00133 (0.000577) s'

    def test_summary_time_rescaling_ns(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0, 0.0015, 0.002, 0.004]

        with redirect_stdout(out := StringIO()):
            for _ in Timed(range(3), unit='ns'):
                pass
            lines = out.getvalue().strip().split('\n')

        assert lines[-3] == 'total 3 iterations in 4e+06 ns'
        assert lines[-2] == 'min/median/max: 5e+05/1.5e+06/2e+06 ns'
        assert lines[-1] == 'average (std): 1.33e+06 (7.64e+05) ns'

    def test_no_print(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0, 10, 20, 30]

        with redirect_stdout(out := StringIO()):
            timed_animals = Timed(['cat', 'dog', 'parrot'],
                                  iteration_print_fn=None, summary_print_fn=None)
            for a in timed_animals:
                print(a)
            lines = out.getvalue().strip().split('\n')

        assert lines == ['cat', 'dog', 'parrot']
        assert timed_animals.total == 30

    def test_item_type_is_preserved(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0, 1, 2]

        animals = []
        timed_animals = Timed(['cat', 'dog'],
                              iteration_print_fn=None, summary_print_fn=None)
        for animal in timed_animals:
            animals.append(animal)
            assert_type(animal, str)

        assert animals == ['cat', 'dog']

    def test_n_is_deprecated(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0, 1, 2]

        timed_range = Timed(range(2), iteration_print_fn=None, summary_print_fn=None)
        for _ in timed_range:
            pass

        with pytest.warns(DeprecationWarning, match='num_iterations'):
            assert timed_range.n == 2

    def test_iterating_again(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0, 1, 3, 10, 10, 20, 40]
        timed_animals = Timed(['cat', 'dog'], iteration_print_fn=None)

        with redirect_stdout(out := StringIO()):
            assert list(timed_animals) == ['cat', 'dog']
            assert list(timed_animals) == ['cat', 'dog']
            lines = out.getvalue().strip().split('\n')

        assert lines[-3] == 'total 2 iterations in 30 s'
        assert lines[-2] == 'min/median/max: 10/15/20 s'
        assert timed_animals.intervals == [10, 20]
        assert timed_animals.total == 30

    def test_async_iterable(self, counter_mock: Mock) -> None:
        counter_mock.side_effect = [0, 0, 1, 3]

        async def numbers() -> AsyncIterator[int]:
            for i in range(2):
                await asyncio.sleep(0)
                yield i

        async def collect() -> list[int]:
            items = []
            async for number in Timed(numbers()):
                assert_type(number, int)
                items.append(number)
            return items

        with redirect_stdout(out := StringIO()):
            items = asyncio.run(collect())
            lines = out.getvalue().strip().split('\n')

        assert items == [0, 1]
        assert lines[0] == 'iteration    1: 1 s'
        assert lines[1] == 'iteration    2: 2 s'
        assert lines[-3] == 'total 2 iterations in 3 s'
