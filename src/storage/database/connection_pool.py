from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
)

from .connection import Connection


class ConnectionPool(metaclass=ABCMeta):
    @abstractmethod
    def init(self) -> Awaitable[None]: ...

    @abstractmethod
    def destroy(self) -> Awaitable[None]: ...

    @abstractmethod
    def get_connection(self) -> Awaitable[Connection]: ...

    @abstractmethod
    def release_connection(self, connection: Connection) -> None: ...
