from asyncio import (
    Lock,
    TimeoutError,
    Queue,
    wait_for,
    get_event_loop,
)
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
        self.__config = config
        self.__used_connections: list[ManageablePoolConnection] = []
        self.__unused_connections: Queue[ManageablePoolConnection] = Queue()
        self.__get_connection_lock = Lock()

    @property
    def __max_size(self) -> int:
        return self.__config.db_connection_pool_max_size

    @property
    def __get_connection_timeout(self) -> float:
        return self.__config.db_connection_pool_timeout

    async def init(self) -> None:
        if len(self.__used_connections) > 0 or not self.__unused_connections.empty():
            raise RuntimeError('pool is already inited')
        await self.__create_connection_and_add(self.__unused_connections.put_nowait)

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
        connection.acquire()
        self.__used_connections.append(connection)
        self.__get_connection_lock.release()
        return connection

    async def __create_connection(self) -> PoolConnection:
        connection = await self.__create_connection_and_add(self.__used_connections.append)
        connection.acquire()
        return connection

    async def __create_connection_and_add(self, add_to_collection: Callable[[ManageablePoolConnection], None]
                                          ) -> ManageablePoolConnection:
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
