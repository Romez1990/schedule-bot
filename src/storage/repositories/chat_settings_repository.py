from abc import ABCMeta, abstractmethod

from data.fp.task import Task
from data.vector import List
from storage.entities import (
    Chat,
    ChatSettings,
)


class ChatSettingsRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, chat_settings: ChatSettings) -> Task[None]: ...

    @abstractmethod
    def delete(self, chat_settings: ChatSettings) -> Task[None]: ...

    @abstractmethod
    def find_all(self, chat: Chat) -> Task[List[ChatSettings]]: ...
