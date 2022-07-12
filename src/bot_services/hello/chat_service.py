from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
)

from storage.entities import (
    Chat as ChatEntity,
)
from messenger_services.messenger_service import (
    Chat,
)


class ChatService(metaclass=ABCMeta):
    @abstractmethod
    def add_chat(self, chat: Chat) -> Awaitable[None]: ...

    @abstractmethod
    def find(self, chat: Chat) -> Awaitable[ChatEntity]: ...
