from vkwave.bots import SimpleBotEvent

from src.bot_services import (
    UserServiceFactoryInterface,
    UserSettingsServiceInterface,
    SubscriptionServiceInterface,
)

from returns.unsafe import unsafe_perform_io

from ..button_configuration import ButtonConfiguration
from ..text_messages import TextMessagesFactoryInterface
from .vk_bot import VkBot


class VkController:
    def __init__(
            self,
            bot: VkBot,
            button_configuration: ButtonConfiguration,
            text_messages_factory: TextMessagesFactoryInterface,
            user_service_factory: UserServiceFactoryInterface,
            user_settings_service: UserSettingsServiceInterface,
            subscription_service: SubscriptionServiceInterface,
    ) -> None:
        self.__bot = bot
        self.__button_configuration = button_configuration
        self.__text_messages = text_messages_factory.create_plain_text_messages()
        self.__user_service = user_service_factory.create('vk')
        self.__user_settings_service = user_settings_service
        self.__subscription_service = subscription_service

    async def welcome(self, event: SimpleBotEvent) -> None:
        vk_id = self.__get_vk_id(event)
        await self.__user_service.create_if_not_exists(vk_id)
        await event.answer(message=self.__text_messages.start,
                           keyboard=self.__button_configuration.vk_buttons())

    async def help(self, event: SimpleBotEvent) -> None:
        await event.answer(message=self.__text_messages.help,
                           keyboard=self.__button_configuration.vk_buttons())

    async def subscribe(self, event: SimpleBotEvent) -> None:
        vk_id = self.__get_telegram_id(event)
        user = await self.__user_service.find_user(vk_id)
        group_name = event.text.lstrip('/subscribe ')
        result = await (self.__subscription_service.create(user, group_name)
                        .map(lambda _: event.answer(self.__text_messages.subscribe(group_name)))
                        .fix(lambda _: self.__bot.message_handler(vk_id, 'wrong group'))
                        .awaitable())
        await unsafe_perform_io(result.unwrap())

    async def unsubscribe(self, event: SimpleBotEvent) -> None:
        vk_id = self.__get_telegram_id(event)
        user = await self.__user_service.find_user(vk_id)
        group_name = event.text.lstrip('/unsubscribe ')
        result = await (self.__subscription_service.delete(user, group_name)
                        .map(lambda _: event.answer(self.__text_messages.unsubscribe(group_name)))
                        .fix(lambda _: self.__bot.message_handler(vk_id, 'wrong group'))
                        .awaitable())
        await unsafe_perform_io(result.unwrap())

    def __get_vk_id(self, event: SimpleBotEvent) -> str:
        return str(event.object.object.peer_id)
