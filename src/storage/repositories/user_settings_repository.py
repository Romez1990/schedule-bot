from abc import ABCMeta, abstractmethod

from data.fp.task import Task
from data.vector import List
from storage.entities import (
    User,
    UserSettings,
)


class UserSettingsRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, user_settings: UserSettings) -> Task[None]: ...

    @abstractmethod
    def delete(self, user_settings: UserSettings) -> Task[None]: ...

    @abstractmethod
    def find_all(self, user: User) -> Task[List[UserSettings]]: ...
