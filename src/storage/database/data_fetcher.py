from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
    Mapping,
    Type,
    TypeVar,
)

from data.fp.maybe import Maybe
from data.fp.task_either import TaskEither
from .errors import (
    DatabaseError,
)

Record = Mapping[str, object]
Records = Sequence[Record]

T = TypeVar('T')


class DataFetcher(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, query: str, *args: object) -> TaskEither[DatabaseError, None]: ...

    @abstractmethod
    def fetch(self, query: str, *args: object) -> TaskEither[DatabaseError, Records]: ...

    @abstractmethod
    def fetch_row(self, query: str, *args: object) -> TaskEither[DatabaseError, Maybe[Record]]: ...

    @abstractmethod
    def fetch_value(self, query: str, *args: object, value_type: Type[T]) -> TaskEither[DatabaseError, T]: ...
