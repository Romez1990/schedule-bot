from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Awaitable,
    Generic,
    TypeVar,
    TYPE_CHECKING,
)

from .structures import (
    Message,
    User,
    KeyboardBase,
)

if TYPE_CHECKING:
    from .message_handler_decorator import MessageHandlerParameters

T = TypeVar('T')


class MessengerAdapter(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def send_message(self, user: User, text: str, keyboard: KeyboardBase = None) -> Awaitable[None]: ...

    @abstractmethod
    def map_message(self, messenger_message: T) -> Message: ...

    @abstractmethod
    def add_message_handler(self, parameters: MessageHandlerParameters,
                            method: Callable[[T], Awaitable[None]]) -> None: ...
