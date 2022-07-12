from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class GroupSubscription:
    chat_id: int
    group_name: str
    id: int | None = None

    def set_id(self, group_subscription_id: int) -> GroupSubscription:
        return GroupSubscription(self.chat_id, self.group_name, group_subscription_id)
