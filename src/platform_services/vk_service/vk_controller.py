from vkwave.bots import SimpleBotEvent

from .vk_bot import VkBot
from ...general_settings.messages_text import (
    message_text_start,
    message_text_help,
)

from ...general_settings.button_configuration import (
    MENU_VK,
)


class VkController:
    def __init__(self, bot: VkBot) -> None:
        self.__bot = bot

    async def welcome(self, event: SimpleBotEvent) -> None:
        await event.answer(message=message_text_start(),
                           keyboard=MENU_VK.get_keyboard())

    async def help(self, event: SimpleBotEvent) -> None:
        await event.answer(message=message_text_help())
