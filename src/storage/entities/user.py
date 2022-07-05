from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class User:
    messenger: str
    messenger_id: str
    id: int | None = None

    def set_id(self, user_id: int) -> User:
        return User(self.messenger, self.messenger_id, user_id)
