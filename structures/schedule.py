from __future__ import annotations
from typing import List, Dict

from .group import Group
from .group_schedule import GroupSchedule
from .week_day import WeekDay
from .day_schedule import DaySchedule


class Schedule:
    def __init__(self, groups: Dict[Group, GroupSchedule] = None):
        self._groups = {} if groups is None else groups

    @staticmethod
    def group(group: Group, group_schedule: GroupSchedule) -> Schedule:
        return Schedule({
            group: group_schedule
        })

    @staticmethod
    def day(group: Group, day: WeekDay, day_schedule: DaySchedule) -> Schedule:
        return Schedule({
            group: GroupSchedule({
                day: day_schedule
            })
        })

    @property
    def groups(self) -> List[Group]:
        return sorted(self._groups.keys())

    def __getitem__(self, key: Group) -> GroupSchedule:
        return self._groups[key]

    def __setitem__(self, key: Group, value: GroupSchedule) -> None:
        self._groups[key] = value

    def filter(self, groups: List[Group], week_day: WeekDay = None) -> Schedule:
        schedule = Schedule()
        for group in groups:
            if week_day is None:
                schedule[group] = self._groups[group]
            else:
                group_schedule = GroupSchedule()
                group_schedule[week_day] = self._groups[group][week_day]
                schedule[group] = group_schedule
        return schedule
