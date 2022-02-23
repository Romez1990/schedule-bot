from __future__ import annotations

from .entity_base import Entity


class User(Entity):
    def __init__(self, messenger: str, messenger_id: str, user_id: int = None) -> None:
        self.id = user_id
        self.messenger = messenger
        self.messenger_id = messenger_id

    def set_id(self, user_id: int) -> User:
        return User(self.messenger, self.messenger_id, user_id)
