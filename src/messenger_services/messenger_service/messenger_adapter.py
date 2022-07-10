from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Awaitable,
)

from .structures import (
    Message,
    Callback,
    Chat,
    KeyboardBase,
    Payload,
    MessageHandlerParams,
    CallbackHandlerParams,
)


class MessengerAdapter(metaclass=ABCMeta):
    @abstractmethod
    def send_message(self, chat: Chat, text: str, keyboard: KeyboardBase = None) -> Awaitable[None]: ...

    @abstractmethod
    def register_message_handler(self, params: MessageHandlerParams,
                                 handler: Callable[[Message], Awaitable[None]]) -> None: ...

    @abstractmethod
    def register_callback_handler(self, params: CallbackHandlerParams,
                                  handler: Callable[[Callback], Awaitable[None]]) -> None: ...
