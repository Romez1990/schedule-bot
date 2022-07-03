from abc import ABCMeta, abstractmethod
from datetime import date
from typing import (
    Sequence,
)

from data.fp.maybe import Maybe
from data.fp.task import Task


class ScheduleHashStorage(metaclass=ABCMeta):
    @abstractmethod
    def init(self) -> Task[None]: ...

    @abstractmethod
    def get_hashes_by_dates(self, schedule_dates: Sequence[date]) -> Sequence[Maybe[int]]: ...

    @abstractmethod
    def save(self, hashes: Sequence[tuple[date, int]]) -> Task[None]: ...
