from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Awaitable,
    TypeVar,
)

from .messenger_controller import MessengerController
from .messenger_adapter import MessengerAdapter

T = TypeVar('T')


class MessageHandlerAdapter(metaclass=ABCMeta):
    @abstractmethod
    def get_message_handler(self, controller: MessengerController, adapter: MessengerAdapter,
                            method_name: str) -> Callable[[object], Awaitable[None]]: ...
