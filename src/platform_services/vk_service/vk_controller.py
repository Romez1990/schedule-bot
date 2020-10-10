from vkwave.bots import SimpleBotEvent

from .vk_bot import VkBot
from ...general_settings.messages_text import (
    message_text_start,
    message_text_help,
)

from ...general_settings.button_configuration import (
    ButtonConfiguration
)


class VkController:
    def __init__(self, bot: VkBot, vk_button: ButtonConfiguration) -> None:
        self.__bot = bot
        self.vk_button = vk_button

    async def welcome(self, event: SimpleBotEvent) -> None:
        button = self.vk_button.vk_buttons()
        await event.answer(message=message_text_start(),
                           keyboard=button.get_keyboard())

    async def help(self, event: SimpleBotEvent) -> None:
        button = self.vk_button.vk_buttons()
        await event.answer(message=message_text_help(),
                           keyboard=button.get_keyboard())
