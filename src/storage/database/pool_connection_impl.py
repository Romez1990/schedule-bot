from typing import (
    Awaitable,
    Callable,
    Type,
    TypeVar,
)

from data.fp.maybe import Maybe
from data.fp.task_either import TaskEither
from .errors import DatabaseError
from .manageable_pool_connection import ManageablePoolConnection
from .connection import Connection
from .data_fetcher import (
    Records,
    Record,
)

T = TypeVar('T')


class PoolConnectionImpl(ManageablePoolConnection):
    def __init__(self, connection: Connection, on_released: Callable[[], None]) -> None:
        self.__connection = connection
        self.__on_released = on_released
        self.__is_acquired = False

    def __del__(self) -> None:
        if self.__is_acquired:
            raise RuntimeError('connection was not released')

    def acquire(self) -> None:
        self.__check_if_acquired()
        self.__is_acquired = True

    def release(self) -> None:
        self.__check_if_released()
        self.__is_acquired = False
        self.__on_released()

    def open(self) -> Awaitable[None]:
        return self.__connection.open()

    def close(self) -> Awaitable[None]:
        return self.__connection.close()

    def execute(self, query: str, *args: object) -> TaskEither[DatabaseError, None]:
        self.__check_if_released()
        return self.__connection.execute(query, *args)

    def execute_many(self, query: str, *args: object) -> TaskEither[DatabaseError, None]:
        self.__check_if_released()
        return self.__connection.execute_many(query, *args)

    def fetch(self, query: str, *args: object) -> TaskEither[DatabaseError, Records]:
        self.__check_if_released()
        return self.__connection.fetch(query, *args)

    def fetch_row(self, query: str, *args: object) -> TaskEither[DatabaseError, Maybe[Record]]:
        self.__check_if_released()
        return self.__connection.fetch_row(query, *args)

    def fetch_value(self, query: str, *args: object, value_type: Type[T]) -> TaskEither[DatabaseError, T]:
        self.__check_if_released()
        return self.__connection.fetch_value(query, *args, value_type=value_type)

    def __check_if_acquired(self) -> None:
        if self.__is_acquired:
            raise RuntimeError('connection is already acquired')

    def __check_if_released(self) -> None:
        if not self.__is_acquired:
            raise RuntimeError('connection is already released')
