from __future__ import annotations
from datetime import date
from typing import (
    Optional,
    Callable,
    Iterable,
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
        return Schedule(self.week_start, self.week_end, {key: func(value) for key, value in self._data.items()})

    def filter(self, groups: Iterable[Group], day_of_week: DayOfWeek = None) -> Schedule:
        existing_groups = List(groups).filter(self.__group_exists)
        week_schedules = existing_groups \
            .map(self.__get_week_schedule) \
            .map(self.__try_select_day(day_of_week))
        schedule_data = {group: group_schedule for group, group_schedule in zip(existing_groups, week_schedules)}
        return Schedule(self.week_start, self.week_end, schedule_data)

    def __group_exists(self, group: Group) -> bool:
        return group in self._data

    def __get_week_schedule(self, group: Group) -> WeekSchedule:
        return self._data[group]

    def __try_select_day(self, day_of_week: Optional[DayOfWeek]) -> Callable[[WeekSchedule], WeekSchedule]:
        def try_select_day(week_schedule: WeekSchedule) -> WeekSchedule:
            return Maybe.from_optional(day_of_week) \
                .map(self.__select_day(week_schedule)) \
                .get_or(week_schedule)

        return try_select_day

    def __select_day(self, week_schedule: WeekSchedule) -> Callable[[DayOfWeek], WeekSchedule]:
        def select_day(day_of_week: DayOfWeek) -> WeekSchedule:
            day_schedule_index = day_of_week.value - week_schedule.start_from.value
            if not (0 <= day_schedule_index < len(week_schedule)):
                raise RuntimeError(f'there is no {day_of_week} in schedule')
            day_schedule = week_schedule[day_schedule_index]
            day_schedules = [day_schedule]
            return WeekSchedule(day_of_week, day_schedules)

        return select_day
