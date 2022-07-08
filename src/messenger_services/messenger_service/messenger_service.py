from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
    NoReturn,
)

from .messenger_adapter import MessengerAdapter


class MessengerService(metaclass=ABCMeta):
    def __init__(self, adapter: MessengerAdapter) -> None:
        self.__adapter = adapter

    @property
    def adapter(self) -> MessengerAdapter:
        return self.__adapter

    @abstractmethod
    def start(self) -> Awaitable[NoReturn]: ...
