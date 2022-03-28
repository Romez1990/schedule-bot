from abc import ABCMeta, abstractmethod

from .pool_connection import PoolConnection
from .connection import Connection


class ManageablePoolConnection(PoolConnection, Connection, metaclass=ABCMeta):
    @abstractmethod
    def acquire(self) -> None: ...
