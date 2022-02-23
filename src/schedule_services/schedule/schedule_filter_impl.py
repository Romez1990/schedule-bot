from typing import (
    Optional,
    Callable,
    Iterable,
)

from infrastructure.ioc_container import service
from data.fp.maybe import Maybe
from data.vector import List
from .schedule_filter import ScheduleFilter
from .schedule import Schedule
from .week_schedule import WeekSchedule
from .group import Group
from .day_of_week import DayOfWeek


@service
class ScheduleFilterImpl(ScheduleFilter):
    def filter(self, schedule: Schedule, groups: Iterable[Group], day_of_week: DayOfWeek = None) -> Schedule:
        existing_groups = List(groups).filter(self.__group_exists(schedule))
        week_schedules = existing_groups \
            .map(self.__get_week_schedule(schedule)) \
            .map(self.__try_select_day(day_of_week))
        schedule_dict = {group: group_schedule for group, group_schedule in zip(existing_groups, week_schedules)}
        return Schedule(schedule.week_start, schedule.week_end, schedule_dict)

    def __group_exists(self, schedule: Schedule) -> Callable[[Group], bool]:
        def group_exists(group: Group) -> bool:
            return group in schedule

        return group_exists

    def __get_week_schedule(self, schedule: Schedule) -> Callable[[Group], WeekSchedule]:
        def get_week_schedule(group: Group) -> WeekSchedule:
            return schedule[group]

        return get_week_schedule

    def __try_select_day(self, day_of_week: Optional[DayOfWeek]) -> Callable[[WeekSchedule], WeekSchedule]:
        def try_select_day(week_schedule: WeekSchedule) -> WeekSchedule:
            return Maybe.from_optional(day_of_week) \
                .map(self.__select_day(week_schedule)) \
                .get_or(week_schedule)

        return try_select_day

    def __select_day(self, week_schedule: WeekSchedule) -> Callable[[DayOfWeek], WeekSchedule]:
        def select_day(day_of_week: DayOfWeek) -> WeekSchedule:
            day_index = day_of_week.value - week_schedule.starts_from.value
            if not (0 <= day_index < len(week_schedule)):
                raise RuntimeError(f'there is no {day_of_week} in schedule')
            day_schedule = week_schedule[day_index]
            day_schedules = [day_schedule]
            return WeekSchedule(day_of_week, day_schedules)

        return select_day
