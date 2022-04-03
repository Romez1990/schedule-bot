from abc import ABCMeta, abstractmethod

from data.fp.task import Task


class FetchInterval(metaclass=ABCMeta):
    @abstractmethod
    def wait(self) -> Task[None]: ...
