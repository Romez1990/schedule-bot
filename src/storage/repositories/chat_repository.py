from abc import ABCMeta, abstractmethod

from data.fp.task import Task
from data.fp.task_maybe import TaskMaybe
from storage.entities import (
    Chat,
)


class ChatRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, chat: Chat) -> Task[Chat]: ...

    @abstractmethod
    def find(self, messenger: str, messenger_id: int) -> TaskMaybe[Chat]: ...
