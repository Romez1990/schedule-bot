from abc import ABCMeta, abstractmethod

from data.fp.task import Task
from data.fp.task_maybe import TaskMaybe
from storage.entities import (
    User,
)


class UserRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user: User) -> Task[User]: ...

    @abstractmethod
    def find(self, platform: str, platform_id: str) -> TaskMaybe[User]: ...
