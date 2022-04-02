from abc import ABCMeta

from .messenger_adapter import MessengerAdapter
from .user import User


class MessengerController(metaclass=ABCMeta):
    def __init__(self, adapter: MessengerAdapter) -> None:
        self.__adapter = adapter

    async def _send_message(self, user: User, text: str) -> None:
        await self.__adapter.send_message(user, text)
