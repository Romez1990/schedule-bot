from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
    Awaitable,
)

from storage.entities import (
    Chat,
)


class GroupService(metaclass=ABCMeta):
    @abstractmethod
    def get_groups(self, chat: Chat) -> Awaitable[Sequence[str]]: ...

    @abstractmethod
    def add_group(self, chat: Chat, group: str) -> Awaitable[None]: ...

    @abstractmethod
    def delete_group(self, chat: Chat, group: str) -> Awaitable[None]: ...
