from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class Chat:
    messenger: str
    messenger_id: int
    id: int | None = None

    def set_id(self, chat_id: int) -> Chat:
        return Chat(self.messenger, self.messenger_id, chat_id)
