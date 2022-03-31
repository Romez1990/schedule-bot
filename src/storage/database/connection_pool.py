from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
)

from .pool_connection_context_manager import PoolConnectionContextManager


class ConnectionPool(metaclass=ABCMeta):
    @abstractmethod
    def init(self) -> Awaitable[None]: ...

    @abstractmethod
    def get_connection(self) -> PoolConnectionContextManager: ...
