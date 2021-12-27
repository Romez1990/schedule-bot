from datetime import date
from collections.abc import Mapping
from typing import (
    Iterator,
    TypeVar,
    Generic,
)

from .group import Group

T = TypeVar('T')


class ScheduleBase(Mapping[Group, T], Generic[T]):
    def __init__(self, week_start: date, week_end: date, data: Mapping[Group, T]) -> None:
        self.week_end = week_end
        self.week_start = week_start
        self.__data = data

    def __iter__(self) -> Iterator[Group]:
        return iter(self.__data)

    def __getitem__(self, key: Group) -> T:
        return self.__data[key]

    def __len__(self) -> int:
        return len(self.__data)
