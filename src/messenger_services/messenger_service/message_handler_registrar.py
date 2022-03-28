from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
    NoReturn,
)

from infrastructure.ioc_container import Container


class MessageHandlerRegistrar(metaclass=ABCMeta):
    @abstractmethod
    def register(self, container: Container) -> None: ...

    @abstractmethod
    def start(self) -> Awaitable[NoReturn]: ...
