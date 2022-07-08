from dataclasses import dataclass

from .chat import Chat


@dataclass(frozen=True, eq=False)
class Message:
    chat: Chat
    text: str
