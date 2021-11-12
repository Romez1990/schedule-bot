from itertools import dropwhile
from returns.maybe import Nothing

from src.schedule import (
    Schedule,
    GroupSchedule,
    DaySchedule,
    DayOfWeek,
)
from src.functions import (
    pipe2,
)
from .schedule_post_processor_interface import SchedulePostProcessorInterface


class SchedulePostProcessor(SchedulePostProcessorInterface):
    def process(self, schedule: Schedule) -> Schedule:
        return pipe2(
            schedule,
            self.__remove_trailing_nothing_entries,
            self.__remove_weekend_if_empty,
        )

    def __remove_trailing_nothing_entries(self, schedule: Schedule) -> Schedule:
        return schedule.map(self.__remove_trailing_nothing_entries_from_group_schedule)

    def __remove_trailing_nothing_entries_from_group_schedule(self, group_schedule: GroupSchedule) -> GroupSchedule:
        return group_schedule.map(self.__remove_trailing_nothing_entries_from_day_schedule)

    def __remove_trailing_nothing_entries_from_day_schedule(self, day_schedule: DaySchedule) -> DaySchedule:
        if not day_schedule:
            return DaySchedule([Nothing])

        dropped = dropwhile(lambda entry: entry == Nothing, reversed(day_schedule))
        return DaySchedule(reversed(list(dropped)))

    def __remove_weekend_if_empty(self, schedule: Schedule) -> Schedule:
        return schedule.map(self.__remove_weekend_if_empty_from_group_schedule)

    def __remove_weekend_if_empty_from_group_schedule(self, group_schedule: GroupSchedule) -> GroupSchedule:
        return pipe2(
            group_schedule,
            lambda schedule: self.__remove_day_if_empty(schedule, DayOfWeek.saturday),
            lambda schedule: self.__remove_day_if_empty(schedule, DayOfWeek.sunday),
        )

    def __remove_day_if_empty(self, group_schedule: GroupSchedule, weekday: DayOfWeek) -> GroupSchedule:
        day_schedule = group_schedule.get(weekday)
        if day_schedule is None or bool(day_schedule):
            return group_schedule
        return group_schedule.remove(weekday)
