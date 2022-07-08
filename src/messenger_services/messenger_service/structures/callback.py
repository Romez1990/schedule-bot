from dataclasses import dataclass
from typing import (
    Callable,
    Awaitable,
)

from .message import Message


@dataclass(frozen=True, eq=False)
class Callback:
    message: Message
    answer: Callable[[str], Awaitable[None]]
