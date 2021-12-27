from itertools import dropwhile

from infrastructure.ioc_container import service
from data.fp.maybe import Nothing
from schedule_services.schedule import (
    Schedule,
    WeekSchedule,
    DaySchedule,
    DayOfWeek,
)
from .schedule_post_processor import SchedulePostProcessor


@service
class SchedulePostProcessorImpl(SchedulePostProcessor):
    def process(self, schedule: Schedule) -> Schedule:
        new_schedule = schedule
        new_schedule = self.__remove_trailing_nothing_entries(new_schedule)
        new_schedule = self.__remove_weekend_if_empty(new_schedule)
        return new_schedule

    def __remove_trailing_nothing_entries(self, schedule: Schedule) -> Schedule:
        return schedule.map(self.__remove_trailing_nothing_entries_from_group_schedule)

    def __remove_trailing_nothing_entries_from_group_schedule(self, group_schedule: WeekSchedule) -> WeekSchedule:
        return group_schedule.map(self.__remove_trailing_nothing_entries_from_day_schedule)

    def __remove_trailing_nothing_entries_from_day_schedule(self, day_schedule: DaySchedule) -> DaySchedule:
        if not day_schedule:
            return DaySchedule([Nothing])

        dropped = dropwhile(lambda entry: entry == Nothing, reversed(day_schedule))
        return DaySchedule(reversed(list(dropped)))

    def __remove_weekend_if_empty(self, schedule: Schedule) -> Schedule:
        return schedule.map(self.__remove_weekend_if_empty_from_group_schedule)

    def __remove_weekend_if_empty_from_group_schedule(self, group_schedule: WeekSchedule) -> WeekSchedule:
        new_group_schedule = group_schedule
        new_group_schedule = self.__remove_day_if_empty(new_group_schedule, DayOfWeek.sunday)
        new_group_schedule = self.__remove_day_if_empty(new_group_schedule, DayOfWeek.saturday)
        return new_group_schedule

    def __remove_day_if_empty(self, group_schedule: WeekSchedule, weekday: DayOfWeek) -> WeekSchedule:
        day_schedule = group_schedule[weekday]
        if day_schedule is None or bool(day_schedule):
            return group_schedule
        return group_schedule.remove(weekday)
