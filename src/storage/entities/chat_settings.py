from __future__ import annotations
from dataclasses import dataclass

from .chat import Chat


@dataclass(frozen=True, eq=False)
class ChatSettings:
    chat: Chat
    name: str
    value: str
    id: int | None = None

    def set_id(self, chat_settings_id: int) -> ChatSettings:
        return ChatSettings(self.chat, self.name, self.value, chat_settings_id)
