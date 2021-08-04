from typing import (
    Callable,
    Type,
    TypeVar,
)

from infrastructure.ioc_container import service
from data.fp.maybe import Maybe
from data.fp.either import Either, Right
from data.fp.task import Task
from data.fp.task_either import TaskEither
from .errors import (
    DatabaseError,
)
from .database import Database
from .connection_pool import ConnectionPool
from .pool_connection import PoolConnection
from .data_fetcher import (
    Records,
    Record,
)

T = TypeVar('T')


@service
class DatabaseImpl(Database):
    def __init__(self, connection_pool: ConnectionPool) -> None:
        self.__connection_pool = connection_pool

    async def connect(self) -> None:
        await self.__connection_pool.init()

    async def disconnect(self) -> None:
        await self.__connection_pool.destroy()

    def execute(self, query: str, *args: object) -> TaskEither[DatabaseError, None]:
        def perform_query(connection: PoolConnection) -> TaskEither[DatabaseError, None]:
            return connection.execute(query, *args)

        return self.__with_connection(perform_query)

    def fetch(self, query: str, *args: object) -> TaskEither[DatabaseError, Records]:
        def perform_query(connection: PoolConnection) -> TaskEither[DatabaseError, Records]:
            return connection.fetch(query, *args)

        return self.__with_connection(perform_query)

    def fetch_row(self, query: str, *args: object) -> TaskEither[DatabaseError, Maybe[Record]]:
        def perform_query(connection: PoolConnection) -> TaskEither[DatabaseError, Maybe[Record]]:
            return connection.fetch_row(query, *args)

        return self.__with_connection(perform_query)

    def fetch_value(self, query: str, *args: object, value_type: Type[T]) -> TaskEither[DatabaseError, T]:
        def perform_query(connection: PoolConnection) -> TaskEither[DatabaseError, object]:
            return connection.fetch_value(query, *args, value_type=value_type)

        return self.__with_connection(perform_query)

    def __with_connection(self, perform_query: Callable[[PoolConnection], TaskEither[DatabaseError, T]],
                          ) -> TaskEither[DatabaseError, T]:
        def perform_query_and_release(connection: PoolConnection) -> TaskEither[DatabaseError, T]:
            def release_connection(result: Either[DatabaseError, T]) -> Either[DatabaseError, T]:
                self.__connection_pool.release_connection(connection)
                return result

            return perform_query(connection) \
                .map_task(release_connection)

        get_connection_task: Task[Either[DatabaseError, PoolConnection]] = Task(self.__connection_pool.get_connection()) \
            .map(Right)
        return TaskEither(get_connection_task) \
            .bind(perform_query_and_release)

    def __right_connection(self, connection: PoolConnection) -> Either[Exception, PoolConnection]:
        return Right(connection)
