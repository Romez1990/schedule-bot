from abc import ABCMeta, abstractmethod
from datetime import date
from typing import (
    Sequence,
    Mapping,
)

from data.fp.maybe import Maybe
from data.fp.task import Task
from schedule_services.schedule import Group


class GroupScheduleHashStorage(metaclass=ABCMeta):
    @abstractmethod
    def init(self) -> Task[None]: ...

    @abstractmethod
    def get_hashes_by_dates(self, schedule_dates: Sequence[tuple[date, Sequence[Group]]]
                            ) -> Sequence[Mapping[Group, Maybe[int]]]: ...

    @abstractmethod
    def save(self, hashes: Sequence[tuple[date, Sequence[tuple[Group, int]]]]) -> Task[None]: ...
