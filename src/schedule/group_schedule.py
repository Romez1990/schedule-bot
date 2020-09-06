from __future__ import annotations
from typing import (
    Iterator,
    Mapping,
)
from pyrsistent import pmap, PMap

from .week_day import WeekDay
from .day_schedule import DaySchedule


class GroupSchedule(Mapping[WeekDay, DaySchedule]):
    def __init__(self, day_schedules: Mapping[WeekDay, DaySchedule]):
        self.__day_schedules = pmap(day_schedules)

    __day_schedules: PMap[WeekDay, DaySchedule]

    def __iter__(self) -> Iterator[WeekDay]:
        return iter(self.__day_schedules)

    def __getitem__(self, key: WeekDay) -> DaySchedule:
        return self.__day_schedules[key]

    def __len__(self) -> int:
        return len(self.__day_schedules)
