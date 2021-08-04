from typing import (
    Callable,
)

from .pool_connection_factory import PoolConnectionFactory
from .manageable_pool_connection import ManageablePoolConnection
from .connection_factory import ConnectionFactory
from .pool_connection_impl import PoolConnectionImpl


class PoolConnectionFactoryImpl(PoolConnectionFactory):
    def __init__(self, connection_factory: ConnectionFactory) -> None:
        self.__connection_factory = connection_factory

    def create(self, on_released: Callable[[], None]) -> ManageablePoolConnection:
        connection = self.__connection_factory.create()
        return PoolConnectionImpl(connection, on_released)
