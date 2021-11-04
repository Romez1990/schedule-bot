from datetime import date
from collections.abc import Mapping
from typing import (
    Iterator,
    TypeVar,
    Generic,
)

T = TypeVar('T')


class ScheduleBase(Generic[T], Mapping[str, T]):
    def __init__(self, week_start: date, week_end: date, data: Mapping[str, T]) -> None:
        self.week_end = week_end
        self.week_start = week_start
        self.__data = data

    def __iter__(self) -> Iterator[str]:
        return iter(self.__data)

    def __len__(self) -> int:
        return len(self.__data)

    def __getitem__(self, key: str) -> T:
        return self.__data[key]
