from src.schedule import (
    Schedule,
    DayOfWeek,
)


class ScheduleMetrics:
    def __init__(self, schedule: Schedule):
        self.groups = len(schedule)
        self._days_length: dict[DayOfWeek, int] = {}
        self.days_offsets: dict[DayOfWeek, int] = {}
        self._compute_days_metrics(schedule)
        self.entries = sum(self._days_length.values())

    def _compute_days_metrics(self, schedule: Schedule) -> None:
        current_offset = 0
        for day_of_week in DayOfWeek:
            max_day_length = 0
            for group in schedule:
                group_schedule = schedule[group]
                try:
                    day = group_schedule[day_of_week]
                except KeyError:
                    continue
                if max_day_length < len(day):
                    max_day_length = len(day)
            if max_day_length != 0:
                self._days_length[day_of_week] = max_day_length
                self.days_offsets[day_of_week] = current_offset
                current_offset += max_day_length

    @property
    def days_of_week(self) -> list[DayOfWeek]:
        return list(self._days_length.keys())

    def __getitem__(self, day: DayOfWeek) -> int:
        return self._days_length[day]
