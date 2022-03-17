from datetime import date
from typing import (
    Mapping,
)

from .schedule_base import ScheduleBase
from .week_schedule import WeekSchedule
from .group import Group


class Schedule(ScheduleBase[WeekSchedule]):
    def __init__(self, week_start: date, schedule: Mapping[Group, WeekSchedule]) -> None:
        super().__init__(week_start, schedule)
