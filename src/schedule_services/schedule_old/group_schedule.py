from __future__ import annotations
from typing import (
    Callable,
    Iterator,
    Mapping,
)

from src.immutable_collections import (
    Dict,
)
from .day_of_week import DayOfWeek
from .day_schedule import DaySchedule


class GroupSchedule(Mapping[DayOfWeek, DaySchedule]):
    def __init__(self, day_schedules: Mapping[DayOfWeek, DaySchedule]) -> None:
        self.__day_schedules = Dict(day_schedules)

    def __iter__(self) -> Iterator[DayOfWeek]:
        return iter(self.__day_schedules)

    def __getitem__(self, key: DayOfWeek) -> DaySchedule:
        return self.__day_schedules[key]

    def remove(self, key: DayOfWeek) -> GroupSchedule:
        return GroupSchedule(self.__day_schedules.remove(key))

    def __len__(self) -> int:
        return len(self.__day_schedules)

    def map(self, func: Callable[[DaySchedule], DaySchedule]) -> GroupSchedule:
        return GroupSchedule({key: func(value) for key, value in self.__day_schedules.items()})
