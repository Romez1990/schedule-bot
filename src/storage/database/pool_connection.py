from abc import ABCMeta, abstractmethod

from .data_fetcher import DataFetcher


class PoolConnection(DataFetcher, metaclass=ABCMeta):
    @abstractmethod
    def release(self) -> None: ...
