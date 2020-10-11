from vkwave.bots import SimpleBotEvent

from ..button_configuration import ButtonConfiguration
from ..messages_text import MessageText
from .vk_bot import VkBot


class VkController:
    def __init__(self, bot: VkBot, vk_button: ButtonConfiguration, message_text: MessageText) -> None:
        self.__bot = bot
        self.__vk_button = vk_button
        self.__message_text = message_text

    async def welcome(self, event: SimpleBotEvent) -> None:
        button = self.__vk_button.vk_buttons()
        await event.answer(message=self.__message_text.message_text_start(),
                           keyboard=button.get_keyboard())

    async def help(self, event: SimpleBotEvent) -> None:
        button = self.__vk_button.vk_buttons()
        await event.answer(message=self.__message_text.message_text_help(),
                           keyboard=button.get_keyboard())
