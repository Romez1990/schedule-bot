from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
)


class FetchInterval(metaclass=ABCMeta):
    @abstractmethod
    def wait(self) -> Awaitable[None]: ...
