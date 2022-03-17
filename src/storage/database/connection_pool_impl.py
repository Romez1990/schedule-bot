from asyncio import (
    Lock,
    Future,
    TimeoutError,
    wait_for,
)
from collections import deque
from typing import (
    MutableSequence,
    cast,
)

from infrastructure.ioc_container import service
from infrastructure.config import Config
from data.fp.maybe import Maybe
from .errors import (
    GetConnectionTimeoutError,
)
from .connection_pool import ConnectionPool
from .manageable_pool_connection import ManageablePoolConnection
from .pool_connection import PoolConnection
from .pool_connection_factory import PoolConnectionFactory
from .pool_connection_context_manager import PoolConnectionContextManager


@service
class ConnectionPoolImpl(ConnectionPool):
    def __init__(self, connection_factory: PoolConnectionFactory, config: Config) -> None:
        self.__connection_factory = connection_factory
        self.__max_size = config.db_connection_pool_max_size
        self.__get_connection_timeout = config.db_connection_pool_timeout
        self.__used_connections: list[ManageablePoolConnection] = []
        self.__unused_connections: list[ManageablePoolConnection] = []
        self.__waiting_queue: deque[Future[PoolConnection]] = deque()
        self.__get_connection_lock = Lock()

    async def init(self) -> None:
        await self.__create_connection_and_add_to(self.__unused_connections)

    async def destroy(self) -> None:
        connections = self.__used_connections + self.__unused_connections
        for connection in connections:
            await connection.close()

    def get_connection(self) -> PoolConnectionContextManager:
        async def async_get_connection() -> PoolConnection:
            await self.__get_connection_lock.acquire()
            unused_is_empty = len(self.__unused_connections) == 0
            if unused_is_empty and len(self.__used_connections) < self.__max_size:
                return await self.__create_connection()
            if unused_is_empty and len(self.__used_connections) == self.__max_size:
                self.__get_connection_lock.release()
                return await self.__wait_for_connection()
            return self.__get_unused_connection()

        return PoolConnectionContextManager(async_get_connection())

    def __get_unused_connection(self) -> PoolConnection:
        connection = self.__unused_connections.pop()
        self.__used_connections.append(connection)
        self.__get_connection_lock.release()
        return connection

    async def __create_connection(self) -> PoolConnection:
        return await self.__create_connection_and_add_to(self.__used_connections)

    async def __create_connection_and_add_to(self,
                                             collection: MutableSequence[ManageablePoolConnection]) -> PoolConnection:
        def release_connection() -> None:
            self.release_connection(connection)

        connection = self.__connection_factory.create(release_connection)
        collection.append(connection)
        if self.__get_connection_lock.locked():
            self.__get_connection_lock.release()
        await connection.open()
        return connection

    async def __wait_for_connection(self) -> PoolConnection:
        future: Future[PoolConnection] = Future()
        self.__waiting_queue.append(future)
        try:
            connection = await wait_for(future, self.__get_connection_timeout)
        except TimeoutError:
            raise GetConnectionTimeoutError(self.__get_connection_timeout)
        return connection

    def release_connection(self, connection: PoolConnection) -> None:
        def get_from_queue() -> Future[PoolConnection]:
            return self.__waiting_queue.popleft()

        def pass_connection(waiting: Future[PoolConnection]) -> None:
            # is doesn't move from used_connections to unused_connections because connection is passed to another use
            waiting.set_result(connection)

        def release_connection() -> None:
            manageable_pool_connection = cast(ManageablePoolConnection, connection)
            self.__used_connections.remove(manageable_pool_connection)
            self.__unused_connections.append(manageable_pool_connection)

        Maybe.try_except(get_from_queue, IndexError) \
            .match(release_connection, pass_connection)
