from abc import ABCMeta

from .structures import (
    User,
)
from .messenger_adapter import MessengerAdapter


class MessengerController(metaclass=ABCMeta):
    def __init__(self, adapter: MessengerAdapter) -> None:
        self.__adapter = adapter

    async def _send_message(self, user: User, text: str) -> None:
        await self.__adapter.send_message(user, text)
