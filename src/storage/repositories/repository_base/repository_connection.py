from abc import ABCMeta, abstractmethod
from typing import (
    Type,
    TypeVar,
)

from data.fp.maybe import Maybe
from data.fp.task import Task
from storage.database import (
    Records,
    Record,
)

T = TypeVar('T')


class RepositoryConnection(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, query: str, *args: object) -> Task[None]: ...

    @abstractmethod
    def execute_many(self, query: str, *args: object) -> Task[None]: ...

    @abstractmethod
    def fetch(self, query: str, *args: object) -> Task[Records]: ...

    @abstractmethod
    def fetch_row(self, query: str, *args: object) -> Task[Maybe[Record]]: ...

    @abstractmethod
    def fetch_value(self, query: str, *args: object, value_type: Type[T]) -> Task[T]: ...
