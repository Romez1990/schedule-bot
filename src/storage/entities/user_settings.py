from __future__ import annotations
from dataclasses import dataclass

from .user import User


@dataclass(frozen=True, eq=False)
class UserSettings:
    user: User
    name: str
    value: str
    id: int | None = None

    def set_id(self, user_settings_id: int) -> UserSettings:
        return UserSettings(self.user, self.name, self.value, user_settings_id)
