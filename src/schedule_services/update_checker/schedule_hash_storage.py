from abc import ABCMeta, abstractmethod
from datetime import date
from typing import (
    Sequence,
)

from data.fp.maybe import Maybe
from data.fp.task import Task


class ScheduleHashStorage(metaclass=ABCMeta):
    @abstractmethod
    def get_hashes_by_date(self, schedule_dates: Sequence[date]) -> Task[Sequence[Maybe[int]]]: ...

    @abstractmethod
    def save(self, hashes: Sequence[tuple[date, int]]) -> Task[None]: ...
