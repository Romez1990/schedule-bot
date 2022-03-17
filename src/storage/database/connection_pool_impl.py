from asyncio import (
    Lock,
    TimeoutError,
    Queue,
    wait_for,
)
from itertools import chain
from typing import (
    Callable,
    cast,
)

from infrastructure.ioc_container import service
from infrastructure.config import Config
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
        self.__unused_connections: Queue[ManageablePoolConnection] = Queue()
        self.__get_connection_lock = Lock()

    async def init(self) -> None:
        await self.__create_connection_and_add(self.__unused_connections.put_nowait)

    async def destroy(self) -> None:
        connections = chain(self.__used_connections, self.__unused_connections)
        for connection in connections:
            await connection.close()

    def get_connection(self) -> PoolConnectionContextManager:
        async def async_get_connection() -> PoolConnection:
            await self.__get_connection_lock.acquire()
            unused_is_empty = self.__unused_connections.empty()
            if unused_is_empty and len(self.__used_connections) < self.__max_size:
                return await self.__create_connection()
            if unused_is_empty and len(self.__used_connections) == self.__max_size:
                self.__get_connection_lock.release()
                return await self.__wait_for_connection()
            return self.__get_unused_connection()

        return PoolConnectionContextManager(async_get_connection())

    def __get_unused_connection(self) -> PoolConnection:
        connection = self.__unused_connections.get_nowait()
        self.__used_connections.append(connection)
        self.__get_connection_lock.release()
        return connection

    async def __create_connection(self) -> PoolConnection:
        return await self.__create_connection_and_add(self.__used_connections.append)

    async def __create_connection_and_add(self, add_to_collection: Callable[[ManageablePoolConnection], None]
                                          ) -> PoolConnection:
        def release_connection() -> None:
            self.release_connection(connection)

        connection = self.__connection_factory.create(release_connection)
        add_to_collection(connection)
        if self.__get_connection_lock.locked():
            self.__get_connection_lock.release()
        await connection.open()
        return connection

    async def __wait_for_connection(self) -> PoolConnection:
        try:
            connection = await wait_for(self.__unused_connections.get(), self.__get_connection_timeout)
        except TimeoutError:
            raise GetConnectionTimeoutError(self.__get_connection_timeout)
        return connection

    def release_connection(self, connection: PoolConnection) -> None:
        manageable_pool_connection = cast(ManageablePoolConnection, connection)
        self.__used_connections.remove(manageable_pool_connection)
        self.__unused_connections.put_nowait(manageable_pool_connection)
