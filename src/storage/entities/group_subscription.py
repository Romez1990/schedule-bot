from __future__ import annotations

from .entity_base import Entity
from .user import User


class GroupSubscription(Entity):
    def __init__(self, user: User, group_name: str, id: int = None) -> None:
        self.id = id
        self.user = user
        self.group_name = group_name

    def set_id(self, group_subscription_id: int) -> GroupSubscription:
        return GroupSubscription(self.user, self.group_name, group_subscription_id)
