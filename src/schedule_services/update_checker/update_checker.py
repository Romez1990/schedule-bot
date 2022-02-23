from abc import ABCMeta, abstractmethod
from typing import (
    NoReturn,
    Awaitable,
)


class UpdateChecker(metaclass=ABCMeta):
    @abstractmethod
    def start(self) -> Awaitable[NoReturn]: ...
