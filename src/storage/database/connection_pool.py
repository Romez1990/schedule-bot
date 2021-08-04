from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
)

from .pool_connection_context_manager import PoolConnectionContextManager
from .pool_connection import PoolConnection


class ConnectionPool(metaclass=ABCMeta):
    @abstractmethod
    def init(self) -> Awaitable[None]: ...

    @abstractmethod
    def destroy(self) -> Awaitable[None]: ...

    @abstractmethod
    def get_connection(self) -> PoolConnectionContextManager: ...

    @abstractmethod
    def release_connection(self, connection: PoolConnection) -> None: ...
