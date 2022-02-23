from abc import ABCMeta, abstractmethod
from typing import (
    NoReturn,
    Awaitable,
)


class ScheduleFetcher(metaclass=ABCMeta):
    @abstractmethod
    def start(self) -> Awaitable[NoReturn]: ...
