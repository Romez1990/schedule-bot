from abc import ABCMeta
from typing import (
    TypeVar,
)

from storage.database import (
    ConnectionPool,
)
from .repository_connection_factory import RepositoryConnectionFactory
from .repository_connection_context_manager import RepositoryConnectionContextManager
from .manageable_repository_connection import ManageableRepositoryConnection

T = TypeVar('T')


class RepositoryBase(metaclass=ABCMeta):
    def __init__(self, connection_pool: ConnectionPool,
                 repository_connection_factory: RepositoryConnectionFactory) -> None:
        self.__connection_pool = connection_pool
        self.__repository_connection_factory = repository_connection_factory

    def _get_connection(self) -> RepositoryConnectionContextManager:
        return RepositoryConnectionContextManager(self.__get_connection_async())

    async def __get_connection_async(self) -> ManageableRepositoryConnection:
        connection = await self.__connection_pool.get_connection()
        return self.__repository_connection_factory.create(connection)
