from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Awaitable,
)

from .structures import (
    Message,
    User,
    KeyboardBase,
    MessageHandlerParams,
)


class MessengerAdapter(metaclass=ABCMeta):
    @abstractmethod
    def send_message(self, user: User, text: str, keyboard: KeyboardBase = None) -> Awaitable[None]: ...

    @abstractmethod
    def register_message_handler(self, params: MessageHandlerParams,
                                 handler: Callable[[Message], Awaitable[None]]) -> None: ...
