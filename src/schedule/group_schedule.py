from __future__ import annotations
from typing import (
    Iterator,
    Mapping,
)
from pyrsistent import pmap, PMap

from .day_of_week import DayOfWeek
from .day_schedule import DaySchedule


class GroupSchedule(Mapping[DayOfWeek, DaySchedule]):
    def __init__(self, day_schedules: Mapping[DayOfWeek, DaySchedule]) -> None:
        self.__day_schedules = pmap(day_schedules)

    __day_schedules: PMap[DayOfWeek, DaySchedule]

    def __iter__(self) -> Iterator[DayOfWeek]:
        return iter(self.__day_schedules)

    def __getitem__(self, key: DayOfWeek) -> DaySchedule:
        return self.__day_schedules[key]

    def __len__(self) -> int:
        return len(self.__day_schedules)
