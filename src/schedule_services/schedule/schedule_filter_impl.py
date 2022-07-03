from typing import (
    Iterable,
    Callable,
)

from infrastructure.ioc_container import service
from data.fp.maybe import Maybe
from data.vector import List
from .schedule_filter import ScheduleFilter
from .schedule import Schedule
from .group_schedule import GroupSchedule
from .group import Group
from .day_of_week import DayOfWeek
from .day_schedule import DaySchedule


@service
class ScheduleFilterImpl(ScheduleFilter):
    def filter(self, schedule: Schedule, groups: Iterable[Group], day_of_week: DayOfWeek = None) -> Schedule:
        group_schedules = List(groups) \
            .map(self.__get_group_schedule(schedule)) \
            .map(self.__select_day_if_specified(day_of_week))
        schedule_dict = {group: group_schedule for group, group_schedule in zip(groups, group_schedules)}
        return Schedule(schedule.starts_at, schedule_dict)

    def __get_group_schedule(self, schedule: Schedule) -> Callable[[Group], GroupSchedule]:
        def get_group_schedule(group: Group) -> GroupSchedule:
            return schedule[group]

        return get_group_schedule

    def __select_day_if_specified(self, day_of_week: DayOfWeek | None) -> Callable[[GroupSchedule], GroupSchedule]:
        def try_select_day(group_schedule: GroupSchedule) -> GroupSchedule:
            return Maybe.from_optional(day_of_week) \
                .map(self.__select_day(group_schedule)) \
                .get_or(group_schedule)

        return try_select_day

    def __select_day(self, group_schedule: GroupSchedule) -> Callable[[DayOfWeek], GroupSchedule]:
        def select_day(day_of_week: DayOfWeek) -> GroupSchedule:
            day_index = day_of_week.value - group_schedule.starts_from.value
            day_schedule = group_schedule[day_index] if 0 <= day_index < len(group_schedule) else DaySchedule.empty
            return GroupSchedule(day_of_week, [day_schedule])

        return select_day
