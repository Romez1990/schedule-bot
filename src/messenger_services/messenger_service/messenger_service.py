from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Awaitable,
    Coroutine,
)

from .messenger_adapter import MessengerAdapter
from .messege_handler_parameters import MessageHandlerParameters


class MessengerService(metaclass=ABCMeta):
    def __init__(self, adapter: MessengerAdapter) -> None:
        self.__adapter = adapter

    @property
    def adapter(self) -> MessengerAdapter:
        return self.__adapter

    def add_message_handler(self, parameters: MessageHandlerParameters,
                            method: Callable[[object], Awaitable[None]]) -> None:
        self.adapter.add_message_handler(parameters, method)

    @abstractmethod
    def start(self) -> Coroutine[object, None, None]: ...
