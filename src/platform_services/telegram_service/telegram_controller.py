from aiogram.types import (
    Message,
    ParseMode,
)
from returns.unsafe import unsafe_perform_io

from src.bot_services import (
    UserServiceFactoryInterface,
    UserSettingsServiceInterface,
    SubscriptionServiceInterface,
)
from ..messages_text import MessageText
from ..button_configuration import ButtonConfiguration
from .telegram_bot import TelegramBot


class TelegramController:
    def __init__(
            self,
            bot: TelegramBot,
            button_configuration: ButtonConfiguration,
            message_text: MessageText,
            user_service_factory: UserServiceFactoryInterface,
            user_settings_service: UserSettingsServiceInterface,
            subscription_service: SubscriptionServiceInterface,
    ) -> None:
        self.__bot = bot
        self.__button_configuration = button_configuration
        self.__message_text = message_text
        self.__user_service = user_service_factory.create('telegram')
        self.__user_settings_service = user_settings_service
        self.__subscription_service = subscription_service

    async def welcome(self, message: Message) -> None:
        telegram_id = self.__get_telegram_id(message)
        await self.__user_service.create_if_not_exists(telegram_id)
        await self.__bot.send_message(telegram_id, self.__message_text.message_text_start('telegram'),
                                      reply_markup=self.__button_configuration.telegram_buttons(),
                                      parse_mode=ParseMode.HTML)

    async def help(self, message: Message) -> None:
        telegram_id = self.__get_telegram_id(message)
        await self.__bot.send_message(telegram_id, self.__message_text.message_text_help('telegram'),
                                      reply_markup=self.__button_configuration.telegram_buttons(),
                                      parse_mode=ParseMode.HTML)

    async def subscribe(self, message: Message) -> None:
        telegram_id = self.__get_telegram_id(message)
        user = await self.__user_service.find_user(telegram_id)
        group_name = message.text.lstrip('/subscribe ')
        result = await (self.__subscription_service.create(user, group_name)
                        .map(lambda _: self.__bot.send_message(telegram_id, 'ok'))
                        .fix(lambda _: self.__bot.send_message(telegram_id, 'wrong group'))
                        .awaitable())
        await unsafe_perform_io(result.unwrap())

    async def unsubscribe(self, message: Message) -> None:
        telegram_id = self.__get_telegram_id(message)
        user = await self.__user_service.find_user(telegram_id)
        group_name = message.text.lstrip('/unsubscribe ')
        result = await (self.__subscription_service.delete(user, group_name)
                        .map(lambda _: self.__bot.send_message(telegram_id, 'ok'))
                        .fix(lambda _: self.__bot.send_message(telegram_id, 'wrong group'))
                        .awaitable())
        await unsafe_perform_io(result.unwrap())

    def __get_telegram_id(self, message: Message) -> str:
        return str(message.from_user.id)
