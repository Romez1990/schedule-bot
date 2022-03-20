from abc import ABCMeta, abstractmethod
from datetime import date

from data.fp.task import Task
from data.fp.task_maybe import TaskMaybe


class ScheduleHashStorage(metaclass=ABCMeta):
    @abstractmethod
    def get_hash_by_date(self, schedule_date: date) -> TaskMaybe[int]: ...

    @abstractmethod
    def save(self, schedule_date: date, schedule_hash: int) -> Task[None]: ...

    @abstractmethod
    def update_schedule_hash(self, schedule_date: date, schedule_hash: int) -> Task[None]: ...
