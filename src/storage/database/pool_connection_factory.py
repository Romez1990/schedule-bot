from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
)

from .manageable_pool_connection import ManageablePoolConnection


class PoolConnectionFactory(metaclass=ABCMeta):
    @abstractmethod
    def create(self, on_released: Callable[[], None]) -> ManageablePoolConnection: ...
