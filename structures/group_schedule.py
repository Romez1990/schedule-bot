from __future__ import annotations
from typing import Dict, List

from .week_day import WeekDay
from .day_schedule import DaySchedule


class GroupSchedule:
    def __init__(self, days: Dict[WeekDay, DaySchedule] = None):
        self._days = {} if days is None else days

    @staticmethod
    def day(day: WeekDay, day_schedule: DaySchedule) -> GroupSchedule:
        return GroupSchedule({
            day: day_schedule
        })

    @property
    def days(self) -> List[WeekDay]:
        return sorted(self._days.keys())

    def __getitem__(self, key: WeekDay) -> DaySchedule:
        return self._days[key]

    def __setitem__(self, key: WeekDay, value: DaySchedule) -> None:
        self._days[key] = value
