from __future__ import annotations


class User:
    def __init__(self, messenger: str, messenger_id: str, id: int = None) -> None:
        self.id = id
        self.messenger = messenger
        self.messenger_id = messenger_id

    def set_id(self, id: int) -> User:
        return User(self.messenger, self.messenger_id, id)
