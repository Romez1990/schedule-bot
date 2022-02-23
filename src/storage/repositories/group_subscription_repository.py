from abc import ABCMeta, abstractmethod

from data.fp.task import Task
from data.vector import List
from storage.entities import (
    User,
    GroupSubscription,
)


class GroupSubscriptionRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, group_subscription: GroupSubscription) -> Task[None]: ...

    @abstractmethod
    def delete(self, group_subscription: GroupSubscription) -> Task[None]: ...

    @abstractmethod
    def find_all(self, user: User) -> Task[List[GroupSubscription]]: ...
