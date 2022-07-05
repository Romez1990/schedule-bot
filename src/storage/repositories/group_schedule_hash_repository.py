from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
)

from data.fp.task import Task
from storage.entities import GroupScheduleHash


class GroupScheduleHashRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_all(self) -> Task[Sequence[GroupScheduleHash]]: ...

    @abstractmethod
    def save_all(self, schedule_hashes: Sequence[GroupScheduleHash]) -> Task[Sequence[GroupScheduleHash]]: ...

    @abstractmethod
    def update_all(self, schedule_hashes: Sequence[GroupScheduleHash]) -> Task[None]: ...

    @abstractmethod
    def delete_all(self, schedule_hashes: Sequence[GroupScheduleHash]) -> Task[None]: ...
