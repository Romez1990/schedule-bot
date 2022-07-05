from __future__ import annotations
from dataclasses import dataclass

from .user import User


@dataclass(frozen=True, eq=False)
class GroupSubscription:
    user: User
    group_name: str
    id: int | None = None

    def set_id(self, group_subscription_id: int) -> GroupSubscription:
        return GroupSubscription(self.user, self.group_name, group_subscription_id)
