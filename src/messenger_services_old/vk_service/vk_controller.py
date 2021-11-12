from vkwave.bots import SimpleBotEvent

from src.bot_services import (
    UserServiceFactoryInterface,
    UserSettingsServiceInterface,
    SubscriptionServiceInterface,
)

from ..button_configuration import ButtonConfiguration
from ..messages_text import MessageText
from .vk_bot import VkBot


class VkController:
    def __init__(
            self,
            bot: VkBot,
            vk_button: ButtonConfiguration,
            message_text: MessageText,
            user_service_factory: UserServiceFactoryInterface,
            user_settings_service: UserSettingsServiceInterface,
            subscription_service: SubscriptionServiceInterface,
    ) -> None:
        self.__bot = bot
        self.__vk_button = vk_button
        self.__message_text = message_text
        self.__button = vk_button.vk_buttons()
        self.__user_service = user_service_factory.create('vk')
        self.__user_settings_service = user_settings_service
        self.__subscription_service = subscription_service

    async def welcome(self, event: SimpleBotEvent) -> None:
        await event.answer(message=self.__message_text.message_text_start('vk'),
                           keyboard=self.__button.get_keyboard())

    async def help(self, event: SimpleBotEvent) -> None:
        await event.answer(message=self.__message_text.message_text_help('vk'),
                           keyboard=self.__button.get_keyboard())

    def __get_vk_id(self, event: SimpleBotEvent) -> str:
        return str(event.object.object.message.from_id)
