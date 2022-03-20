from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Awaitable,
    Generic,
    TypeVar,
    TYPE_CHECKING,
)

from .user import User
from .message import Message

if TYPE_CHECKING:
    from .message_handler_decorator import MessageHandlerParameters

T = TypeVar('T')


class MessengerAdapter(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def send_message(self, user: User, text: str, keyboard=None) -> Awaitable[None]: ...

    @abstractmethod
    async def send_image(self, user: User, image_bytes: bytes) -> None: ...

    @abstractmethod
    def map_message(self, messenger_message: T) -> Message: ...

    @abstractmethod
    def add_message_handler(self, parameters: MessageHandlerParameters,
                            method: Callable[[T], Awaitable[None]]) -> None: ...
