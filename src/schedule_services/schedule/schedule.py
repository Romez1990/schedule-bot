from __future__ import annotations
from datetime import date
from typing import (
    Optional,
    Callable,
    Iterable,
    Iterator,
    Mapping,
)

from data.fp.maybe import Maybe
from data.vector import (
    List,
    Dict,
)
from .schedule_base import ScheduleBase
from .week_schedule import WeekSchedule
from .group import Group
from .day_of_week import DayOfWeek


class Schedule(ScheduleBase[WeekSchedule]):
    def __init__(self, week_start: date, week_end: date, schedule: Mapping[Group, WeekSchedule]) -> None:
        super().__init__(week_start, week_end, schedule)

    def map(self, func: Callable[[WeekSchedule], WeekSchedule]) -> Schedule:
        return Schedule({key: func(value) for key, value in self.__group_schedules.items()})

    def filter(self, groups: Iterable[Group], day_of_week: DayOfWeek = None) -> Schedule:
        group_schedules = List(groups) \
            .filter(self.__group_exists) \
            .map(self.__get_group_schedule) \
            .map(lambda t: (t[0], self.__try_select_day(t[1], day_of_week)))
        return Schedule({group: group_schedule for group, group_schedule in group_schedules})

    def __group_exists(self, group: Group) -> bool:
        return group in self.__group_schedules

    def __get_group_schedule(self, group: Group) -> tuple[Group, WeekSchedule]:
        return group, self.__group_schedules[group]

    def __try_select_day(self, group_schedule: WeekSchedule, day_of_week: Optional[DayOfWeek]) -> WeekSchedule:
        return Maybe.from_optional(day_of_week) \
            .map(lambda day: WeekSchedule(day, {day: group_schedule[day]})) \
            .get_or(group_schedule)
