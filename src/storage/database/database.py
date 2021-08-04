from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
)

from .data_fetcher import DataFetcher


class Database(DataFetcher, metaclass=ABCMeta):
    @abstractmethod
    def connect(self) -> Awaitable[None]: ...

    @abstractmethod
    def disconnect(self) -> Awaitable[None]: ...
