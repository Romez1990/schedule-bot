from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class User:
    chat_id: int
