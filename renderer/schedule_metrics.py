from typing import Dict, List

from structures import Schedule, WeekDay


class ScheduleMetrics:
    def __init__(self, schedule: Schedule):
        self.groups = len(schedule.groups)
        self._days_length: Dict[WeekDay, int] = {}
        self.days_offsets: Dict[WeekDay, int] = {}
        self._compute_days_metrics(schedule)
        self.entries = sum(self._days_length.values())

    def _compute_days_metrics(self, schedule: Schedule) -> None:
        current_offset = 0
        for week_day in WeekDay:
            max_day_length = 0
            for group in schedule.groups:
                group_schedule = schedule[group]
                try:
                    day = group_schedule[week_day]
                except KeyError:
                    continue
                if max_day_length < len(day):
                    max_day_length = len(day)
            if max_day_length != 0:
                self._days_length[week_day] = max_day_length
                self.days_offsets[week_day] = current_offset
                current_offset += max_day_length

    @property
    def week_days(self) -> List[WeekDay]:
        return list(self._days_length.keys())

    def __getitem__(self, day: WeekDay) -> int:
        return self._days_length[day]
