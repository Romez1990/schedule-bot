from dataclasses import dataclass

from .user import User


@dataclass(frozen=True, eq=False)
class Message:
    user: User
    text: str
