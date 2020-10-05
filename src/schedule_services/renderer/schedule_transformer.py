from typing import (
    List,
    Dict,
)

from src.schedule import (
    Schedule,
    GroupSchedule,
    DayOfWeek,
)
from .schedule_transformer_interface import ScheduleTransformerInterface
from .primitives import RenderScheme


class ScheduleTransformer(ScheduleTransformerInterface):
    def transform(self, schedule: Schedule) -> RenderScheme:
        number_of_entries = self.__get_number_of_entries(schedule)
        return RenderScheme()

    def __get_number_of_entries(self, schedule: Schedule) -> Dict[DayOfWeek, int]:
        number_of_entries_of_groups = [
            self.__get_number_of_entries_by_group_schedule(group_schedule)
            for group_schedule in schedule.values()]
        return {day_of_week: self.__get_max_number_of_entries(number_of_entries_of_groups, day_of_week)
                for day_of_week in DayOfWeek}

    def __get_number_of_entries_by_group_schedule(self, group_schedule: GroupSchedule) -> Dict[DayOfWeek, int]:
        return {day_of_week: self.__get_number_of_entries_by_day_of_week(group_schedule, day_of_week)
                for day_of_week in DayOfWeek}

    def __get_number_of_entries_by_day_of_week(self, group_schedule: GroupSchedule, day_of_week: DayOfWeek) -> int:
        if day_of_week not in group_schedule:
            return 0
        return len(group_schedule[day_of_week])

    def __get_max_number_of_entries(self, number_of_entries_of_groups: List[Dict[DayOfWeek, int]],
                                    day_of_week: DayOfWeek) -> int:
        return max([number_of_entries[day_of_week] for number_of_entries in number_of_entries_of_groups])
