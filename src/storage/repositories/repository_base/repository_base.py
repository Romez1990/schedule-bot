from abc import ABCMeta
from typing import (
    Type,
    TypeVar,
)

from data.fp.maybe import Maybe
from data.fp.task import Task
from data.fp.task_either import TaskEither
from storage.database import (
    Database,
    DatabaseError,
    Records,
    Record,
)

T = TypeVar('T')


class RepositoryBase(metaclass=ABCMeta):
    def __init__(self, database: Database) -> None:
        self.__database = database

    def _execute(self, query: str, *args: object) -> Task[None]:
        future_result = self.__database.execute(query, *args)
        return self.__raise_error(future_result)

    def _fetch(self, query: str, *args: object) -> Task[Records]:
        future_result = self.__database.fetch(query, *args)
        return self.__raise_error(future_result)

    def _fetch_row(self, query: str, *args: object) -> Task[Maybe[Record]]:
        future_result = self.__database.fetch_row(query, *args)
        return self.__raise_error(future_result)

    def _fetch_value(self, query: str, *args: object, value_type: Type[T]) -> Task[T]:
        future_result = self.__database.fetch_value(query, *args, value_type=value_type)
        return self.__raise_error(future_result)

    def __raise_error(self, task_either: TaskEither[DatabaseError, T]) -> Task[T]:
        return task_either.get_or_raise()
