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


@service
class ScheduleFilterImpl(ScheduleFilter):
    def filter(self, schedule: Schedule, groups: Iterable[Group], day_of_week: DayOfWeek = None) -> Schedule:
        existing_groups = List(groups).filter(self.__group_exists(schedule))
        group_schedules = existing_groups \
            .map(self.__get_group_schedule(schedule)) \
            .map(self.__try_select_day(day_of_week))
        schedule_dict = {group: group_schedule for group, group_schedule in zip(existing_groups, group_schedules)}
        return Schedule(schedule.starts_at, schedule_dict)

    def __group_exists(self, schedule: Schedule) -> Callable[[Group], bool]:
        def group_exists(group: Group) -> bool:
            return group in schedule

        return group_exists

    def __get_group_schedule(self, schedule: Schedule) -> Callable[[Group], GroupSchedule]:
        def get_group_schedule(group: Group) -> GroupSchedule:
            return schedule[group]

        return get_group_schedule

    def __try_select_day(self, day_of_week: DayOfWeek | None) -> Callable[[GroupSchedule], GroupSchedule]:
        def try_select_day(group_schedule: GroupSchedule) -> GroupSchedule:
            return Maybe.from_optional(day_of_week) \
                .map(self.__select_day(group_schedule)) \
                .get_or(group_schedule)

        return try_select_day

    def __select_day(self, group_schedule: GroupSchedule) -> Callable[[DayOfWeek], GroupSchedule]:
        def select_day(day_of_week: DayOfWeek) -> GroupSchedule:
            day_index = day_of_week.value - group_schedule.starts_from.value
            if not (0 <= day_index < len(group_schedule)):
                raise RuntimeError(f'there is no {day_of_week} in schedule')
            day_schedule = group_schedule[day_index]
            day_schedules = [day_schedule]
            return GroupSchedule(day_of_week, day_schedules)

        return select_day
