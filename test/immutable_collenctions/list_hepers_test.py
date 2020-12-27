from typing import (
    Callable,
)
from unittest.mock import Mock

from src.immutable_collections import List, lazy_reduce


def test_lazy_reduce() -> None:
    lazy_number_1 = Mock(return_value=11)
    lazy_number_2 = Mock(return_value=22)
    lazy_number_3 = Mock(return_value=33)
    numbers = List([
        lazy_number_1,
        lazy_number_2,
        lazy_number_3,
    ])

    def lazy_add(number1: int, number2: Callable[[], int]) -> int:
        return number1 + number2()

    result = lazy_reduce(lazy_add, numbers)

    assert result == 66
    lazy_number_1.assert_called_once()
    lazy_number_2.assert_called_once()
    lazy_number_3.assert_called_once()
