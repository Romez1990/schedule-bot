from abc import ABCMeta, abstractmethod
from typing import (
    Awaitable,
)

from database.entities import (
    User,
)


class GroupController(metaclass=ABCMeta):
    @abstractmethod
    def add_group(self, user: User, group: str) -> Awaitable[None]: ...
