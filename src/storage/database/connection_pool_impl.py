from asyncio import (
    Lock,
    Future,
    TimeoutError,
    wait_for,
)
from collections import deque
from typing import (
    MutableSequence,
)

from infrastructure.ioc_container import service
from infrastructure.config import Config
from data.fp.maybe import Maybe
from .errors import (
    GetConnectionTimeoutError,
)
from .connection_pool import ConnectionPool
from .connection import Connection
from .connection_factory import ConnectionFactory


@service
class ConnectionPoolImpl(ConnectionPool):
    def __init__(self, connection_factory: ConnectionFactory, config: Config) -> None:
        self.__connection_factory = connection_factory
        self.__max_size = config.db_connection_pool_max_size
        self.__get_connection_timeout = config.db_connection_pool_timeout
        self.__used_connections: list[Connection] = []
        self.__unused_connections: list[Connection] = []
        self.__waiting_queue: deque[Future[Connection]] = deque()
        self.__get_connection_lock = Lock()

    async def init(self) -> None:
        await self.__create_connection_and_add_to(self.__unused_connections)

    async def destroy(self) -> None:
        connections = self.__used_connections + self.__unused_connections
        for connection in connections:
            await connection.close()

    async def get_connection(self) -> Connection:
        await self.__get_connection_lock.acquire()
        unused_is_empty = len(self.__unused_connections) == 0
        if unused_is_empty and len(self.__used_connections) < self.__max_size:
            return await self.__create_connection()
        if unused_is_empty and len(self.__used_connections) == self.__max_size:
            self.__get_connection_lock.release()
            return await self.__wait_for_connection()
        return self.__get_unused_connection()

    def __get_unused_connection(self) -> Connection:
        connection = self.__unused_connections.pop()
        self.__used_connections.append(connection)
        self.__get_connection_lock.release()
        return connection

    async def __create_connection(self) -> Connection:
        return await self.__create_connection_and_add_to(self.__used_connections)

    async def __create_connection_and_add_to(self, collection: MutableSequence[Connection]) -> Connection:
        connection = self.__connection_factory.create()
        collection.append(connection)
        if self.__get_connection_lock.locked():
            self.__get_connection_lock.release()
        await connection.open()
        return connection

    async def __wait_for_connection(self) -> Connection:
        future: Future[Connection] = Future()
        self.__waiting_queue.append(future)
        try:
            connection = await wait_for(future, self.__get_connection_timeout)
        except TimeoutError:
            raise GetConnectionTimeoutError(self.__get_connection_timeout)
        return connection

    def release_connection(self, connection: Connection) -> None:
        def get_waiting() -> Future[Connection]:
            return self.__waiting_queue.popleft()

        def pass_connection(waiting: Future[Connection]) -> None:
            # is doesn't move from used_connections to unused_connections cause connection is passed to another use
            waiting.set_result(connection)

        def release_connection() -> None:
            self.__used_connections.remove(connection)
            self.__unused_connections.append(connection)

        Maybe.try_except(get_waiting, IndexError) \
            .match(release_connection, pass_connection)