from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
)

from storage.entities import (
    Chat,
)


class GroupController(metaclass=ABCMeta):
    @abstractmethod
    def add_group(self, chat: Chat, group: str) -> Awaitable[None]: ...
