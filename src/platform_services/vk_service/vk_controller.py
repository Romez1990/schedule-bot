from vkwave.bots import SimpleBotEvent

from .vk_bot import VkBot
from ...general_settings.messages_text import (
    message_text_start,
    message_text_help,
)


class VkController:
    def __init__(self, bot: VkBot) -> None:
        self.__bot = bot

    async def welcome(self, event: SimpleBotEvent) -> None:
        await event.answer(message_text_start())

    async def help(self, event: SimpleBotEvent) -> None:
        await event.answer(message_text_help())
