from __future__ import annotations

from .entity_base import Entity
from .user import User


class UserSettings(Entity):
    def __init__(self, user: User, name: str, value: str, id: int = None) -> None:
        self.id = id
        self.user = user
        self.name = name
        self.value = value

    def set_id(self, user_settings_id: int) -> UserSettings:
        return UserSettings(self.user, self.name, self.value, user_settings_id)
