from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Awaitable,
    Generic,
    TypeVar,
)

from .structures import (
    Message,
    User,
    KeyboardBase,
    MessageHandlerParams,
)

T = TypeVar('T')


class MessengerAdapter(Generic[T], metaclass=ABCMeta):
    @abstractmethod
    def send_message(self, user: User, text: str, keyboard: KeyboardBase = None) -> Awaitable[None]: ...

    @abstractmethod
    def map_message(self, messenger_message: T) -> Message: ...

    @abstractmethod
    def register_message_handler(self, params: MessageHandlerParams, method: Callable[[T], Awaitable[None]]) -> None: ...
