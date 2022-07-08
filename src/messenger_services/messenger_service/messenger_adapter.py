from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Awaitable,
)

from .structures import (
    Message,
    Chat,
    KeyboardBase,
    MessageHandlerParams,
)


class MessengerAdapter(metaclass=ABCMeta):
    @abstractmethod
    def send_message(self, chat: Chat, text: str, keyboard: KeyboardBase = None) -> Awaitable[None]: ...

    @abstractmethod
    def register_message_handler(self, params: MessageHandlerParams,
                                 handler: Callable[[Message], Awaitable[None]]) -> None: ...
