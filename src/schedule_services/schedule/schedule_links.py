from datetime import date
from typing import (
    Mapping,
)

from .schedule_base import ScheduleBase


class ScheduleLinks(ScheduleBase[str]):
    def __init__(self, week_start: date, week_end: date, group_links: Mapping[str, str]) -> None:
        super().__init__(week_start, week_end, group_links)
