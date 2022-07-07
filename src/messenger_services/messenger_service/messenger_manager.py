from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
    NoReturn,
)

from infrastructure.ioc_container import (
    Container,
)


class MessengerManager(metaclass=ABCMeta):
    @abstractmethod
    def init(self, container: Container) -> None: ...

    @abstractmethod
    def start(self) -> Awaitable[NoReturn]: ...
