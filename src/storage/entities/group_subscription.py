from __future__ import annotations
from dataclasses import dataclass

from .chat import Chat


@dataclass(frozen=True, eq=False)
class GroupSubscription:
    chat: Chat
    group_name: str
    id: int | None = None

    def set_id(self, group_subscription_id: int) -> GroupSubscription:
        return GroupSubscription(self.chat, self.group_name, group_subscription_id)
