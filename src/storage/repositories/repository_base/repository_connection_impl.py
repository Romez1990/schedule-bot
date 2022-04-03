from typing import (
    Type,
    TypeVar,
)

from data.fp.maybe import Maybe
from data.fp.task import Task
from data.fp.task_either import TaskEither
from storage.database import (
    PoolConnection,
    DatabaseError,
    Records,
    Record,
)
from .manageable_repository_connection import ManageableRepositoryConnection

T = TypeVar('T')


class RepositoryConnectionImpl(ManageableRepositoryConnection):
    def __init__(self, connection: PoolConnection) -> None:
        self.__connection = connection

    def release(self) -> None:
        self.__connection.release()

    def execute(self, query: str, *args: object) -> Task[None]:
        future_result = self.__connection.execute(query, *args)
        return self.__raise_error(future_result)

    def execute_many(self, query: str, *args: object) -> Task[None]:
        future_result = self.__connection.execute_many(query, *args)
        return self.__raise_error(future_result)

    def fetch(self, query: str, *args: object) -> Task[Records]:
        future_result = self.__connection.fetch(query, *args)
        return self.__raise_error(future_result)

    def fetch_row(self, query: str, *args: object) -> Task[Maybe[Record]]:
        future_result = self.__connection.fetch_row(query, *args)
        return self.__raise_error(future_result)

    def fetch_value(self, query: str, *args: object, value_type: Type[T]) -> Task[T]:
        future_result = self.__connection.fetch_value(query, *args, value_type=value_type)
        return self.__raise_error(future_result)

    def __raise_error(self, task_either: TaskEither[DatabaseError, T]) -> Task[T]:
        return task_either.get_or_raise()
