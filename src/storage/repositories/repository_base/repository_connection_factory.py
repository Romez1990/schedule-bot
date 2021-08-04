from abc import ABCMeta, abstractmethod

from storage.database import PoolConnection
from .manageable_repository_connection import ManageableRepositoryConnection


class RepositoryConnectionFactory(metaclass=ABCMeta):
    @abstractmethod
    def create(self, pool_connection: PoolConnection) -> ManageableRepositoryConnection: ...
