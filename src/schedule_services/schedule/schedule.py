from datetime import date
from typing import (
    Mapping,
)

from data.repr import repr_dict
from .schedule_base import ScheduleBase
from .group_schedule import GroupSchedule
from .group import Group


class Schedule(ScheduleBase[GroupSchedule]):
    def __init__(self, starts_at: date, schedule: Mapping[Group, GroupSchedule]) -> None:
        super().__init__(starts_at, schedule)

    def __repr__(self) -> str:
        starts_at = repr(self.starts_at)[len('datetime.'):]
        return f'{self.__class__.__name__}({starts_at}, {repr_dict(self)})'
