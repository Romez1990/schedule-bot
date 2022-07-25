from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
)

from data.fp.task import Task
from storage.entities import ScheduleHash


class ScheduleHashRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_all(self) -> Task[Sequence[ScheduleHash]]: ...

    @abstractmethod
    def save_all(self, schedule_hashes: Sequence[ScheduleHash]) -> Task[Sequence[ScheduleHash]]: ...

    @abstractmethod
    def update_all(self, schedule_hashes: Sequence[ScheduleHash]) -> Task[None]: ...

    @abstractmethod
    def delete_all(self, schedule_hashes: Sequence[ScheduleHash]) -> Task[None]: ...
