from datetime import date
from typing import (
    Mapping,
)

from .schedule_base import ScheduleBase
from .group import Group


class ScheduleLinks(ScheduleBase[str]):
    def __init__(self, week_start: date, week_end: date, links: Mapping[Group, str]) -> None:
        super().__init__(week_start, week_end, links)
