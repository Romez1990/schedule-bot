from abc import ABCMeta, abstractmethod

from data.fp.task import Task


class MigrationRun(metaclass=ABCMeta):
    @abstractmethod
    def create_table(self) -> Task[None]: ...

    @abstractmethod
    def create_relationship(self) -> Task[None]: ...
