from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
)

from .data_fetcher import DataFetcher


class Connection(DataFetcher, metaclass=ABCMeta):
    @abstractmethod
    def open(self) -> Awaitable[None]: ...

    @abstractmethod
    def close(self) -> Awaitable[None]: ...
