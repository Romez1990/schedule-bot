from abc import ABCMeta, abstractmethod
from datetime import date
from typing import (
    Sequence,
)

from data.fp.task import Task
from data.fp.task_maybe import TaskMaybe


class ScheduleHashStorage(metaclass=ABCMeta):
    @abstractmethod
    def get_hashes_by_date(self, schedule_dates: Sequence[date]) -> TaskMaybe[int]: ...

    @abstractmethod
    def save(self, schedule_date: date, schedule_hash: int) -> Task[None]: ...
