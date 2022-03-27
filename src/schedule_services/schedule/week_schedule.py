from __future__ import annotations
from collections.abc import Sequence
from typing import (
    Iterable,
)

from data.repr import repr_list
from .day_of_week import DayOfWeek
from .day_schedule import DaySchedule


class WeekSchedule(Sequence[DaySchedule]):
    def __init__(self, starts_from: DayOfWeek, day_schedules: Iterable[DaySchedule]) -> None:
        self.starts_from = starts_from
        self.__day_schedules = tuple(day_schedules)

    def __getitem__(self, index: int | slice) -> DaySchedule:
        return self.__day_schedules[index]

    def __len__(self) -> int:
        return len(self.__day_schedules)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({repr(self.starts_from)}, {repr_list(self.__day_schedules)})'
