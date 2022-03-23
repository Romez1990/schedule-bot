from datetime import date
from typing import (
    Optional,
    Mapping,
)

from .schedule_base import ScheduleBase
from .group import Group


class ScheduleLinks(ScheduleBase[str]):
    def __init__(self, starts_at: Optional[date], links: Mapping[Group, str]) -> None:
        super().__init__(starts_at, links)
