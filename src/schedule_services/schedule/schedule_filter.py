from abc import ABCMeta, abstractmethod
from typing import (
    Iterable,
)

from .schedule import Schedule
from .group import Group
from .day_of_week import DayOfWeek


class ScheduleFilter(metaclass=ABCMeta):
    @abstractmethod
    def filter(self, schedule: Schedule, groups: Iterable[Group], day_of_week: DayOfWeek = None) -> Schedule: ...
