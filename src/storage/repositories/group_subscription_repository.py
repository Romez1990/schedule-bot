from abc import ABCMeta, abstractmethod

from data.fp.task import Task
from data.vector import List
from storage.entities import (
    Chat,
    GroupSubscription,
)


class GroupSubscriptionRepository(metaclass=ABCMeta):
    @abstractmethod
    def find_all_by_chat(self, chat: Chat) -> Task[List[GroupSubscription]]: ...

    @abstractmethod
    def save(self, group_subscription: GroupSubscription) -> Task[None]: ...

    @abstractmethod
    def delete_by_group_name(self, chat: Chat, group_name: str) -> Task[None]: ...
