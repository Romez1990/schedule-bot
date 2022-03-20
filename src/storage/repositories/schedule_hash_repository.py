from abc import ABCMeta, abstractmethod

from data.fp.task import Task


class ScheduleHashRepository(metaclass=ABCMeta):
    @abstractmethod
    def f(self) -> Task: ...
