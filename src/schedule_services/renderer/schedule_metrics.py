from itertools import accumulate
from typing import (
    Callable,
)

from data.vector import List
from schedule_services.schedule import (
    Schedule,
    WeekSchedule,
    DayOfWeek,
)


class ScheduleMetrics:
    def __init__(self, schedule: Schedule):
        self.groups_count = len(schedule)
        self.starts_from = self.__get_starts_from(schedule)
        self.ends_with = self.__get_ends_with(schedule)
        self.days_of_week = self.__get_days_of_week()
        self.days_count = len(self.days_of_week)
        self.day_lengths = self.__get_day_lengths(schedule)
        self.day_offsets = self.__get_day_offsets()
        self.total_entries_count = sum(self.day_lengths)

    def __get_starts_from(self, schedule: Schedule) -> DayOfWeek:
        day_of_week_indexes = List(schedule.values()) \
            .map(self.__get_starts_from_value)
        starts_from_index = min(day_of_week_indexes)
        return DayOfWeek(starts_from_index)

    def __get_starts_from_value(self, week_schedule: WeekSchedule) -> int:
        return week_schedule.starts_from.value

    def __get_ends_with(self, schedule: Schedule) -> DayOfWeek:
        day_of_week_indexes = List(schedule.values()) \
            .map(self.__get_ends_with_value)
        ends_with_index = max(day_of_week_indexes)
        return DayOfWeek(ends_with_index)

    def __get_ends_with_value(self, week_schedule: WeekSchedule) -> int:
        return week_schedule.starts_from.value + len(week_schedule) - 1

    def __get_days_of_week(self) -> List[DayOfWeek]:
        start_day_value = self.starts_from.value
        end_day_value = self.ends_with.value
        return List(range(start_day_value, end_day_value + 1)) \
            .map(DayOfWeek)

    def __get_day_lengths(self, schedule: Schedule) -> List[int]:
        return List(range(self.starts_from.value, self.ends_with.value + 1)) \
            .map(self.__get_day_length(schedule))

    def __get_day_length(self, schedule: Schedule) -> Callable[[int], int]:
        def get_day_length(day_of_week_value: int) -> int:
            day_lengths = List(schedule.values()) \
                .map(self.__get_day_length_from_week_schedule(day_of_week_value))
            return max(day_lengths)

        return get_day_length

    def __get_day_length_from_week_schedule(self, day_of_week_value: int) -> Callable[[WeekSchedule], int]:
        def get_day_length_from_week_schedule(week_schedule: WeekSchedule) -> int:
            day_index = day_of_week_value - week_schedule.starts_from.value
            if not (0 <= day_index < len(week_schedule)):
                return 0
            return len(week_schedule[day_index])

        return get_day_length_from_week_schedule

    def __get_day_offsets(self) -> list[int]:
        offsets = list(accumulate(self.day_lengths, initial=0))
        return offsets[:-1]
