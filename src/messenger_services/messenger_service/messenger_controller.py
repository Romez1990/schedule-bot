from abc import ABCMeta

from .structures import (
    Chat,
    KeyboardBase,
)
from .messenger_adapter import MessengerAdapter


class MessengerController(metaclass=ABCMeta):
    def __init__(self, adapter: MessengerAdapter) -> None:
        self.__adapter = adapter

    async def _send_message(self, chat: Chat, text: str, keyboard: KeyboardBase = None) -> None:
        await self.__adapter.send_message(chat, text, keyboard)
