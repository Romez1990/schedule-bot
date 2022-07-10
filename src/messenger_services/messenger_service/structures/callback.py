from dataclasses import dataclass
from typing import (
    Callable,
    Generic,
    TypeVar,
    Awaitable,
)

from .chat import Chat
from .payload import Payload

TPayload = TypeVar('TPayload', bound=Payload)


@dataclass(frozen=True, eq=False)
class Callback(Generic[TPayload]):
    chat: Chat
    payload: TPayload
    answer: Callable[[str], Awaitable[None]]
