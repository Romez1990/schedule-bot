from abc import ABCMeta

from .structures import (
    User,
    KeyboardBase,
)
from .messenger_adapter import MessengerAdapter


class MessengerController(metaclass=ABCMeta):
    def __init__(self, adapter: MessengerAdapter) -> None:
        self.__adapter = adapter

    async def _send_message(self, user: User, text: str, keyboard: KeyboardBase = None) -> None:
        await self.__adapter.send_message(user, text, keyboard)
