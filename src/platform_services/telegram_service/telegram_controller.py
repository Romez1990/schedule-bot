from aiogram.types import (
    Message,
    ParseMode,
)

from src.bot_services import (
    UserServiceInterface,
    UserSettingsServiceInterface,
    SubscriptionServiceInterface,
)
from .telegram_bot import TelegramBot
from src.general_settings.messages_text import message_text_start, message_text_help
from src.general_settings.button_configuration import buttons
from src.general_settings.button_configuration import ButtonConfiguration


class TelegramController:
    def __init__(
            self,
            bot: TelegramBot,
            user_service: UserServiceInterface,
            user_settings_service: UserSettingsServiceInterface,
            subscription_service: SubscriptionServiceInterface,
            button_configuration: ButtonConfiguration,
    ) -> None:
        self.__bot = bot
        self.__user_service = user_service
        self.__user_settings_service = user_settings_service
        self.__subscription_service = subscription_service
        self.__platform = 'telegram'
        self.button_configuration = button_configuration

    async def welcome(self, message: Message) -> None:
        telegram_id = self.__get_telegram_id(message)
        await self.__user_service.create_if_not_exists(self.__platform, telegram_id)
        await self.__bot.send_message(telegram_id, message_text_start(),
                                      reply_markup=self.button_configuration.telegram_buttons(),
                                      parse_mode=ParseMode.HTML)

    async def help(self, message: Message) -> None:
        telegram_id = self.__get_telegram_id(message)
        await self.__bot.send_message(telegram_id, message_text_help(),
                                      reply_markup=self.button_configuration.telegram_buttons(),
                                      parse_mode=ParseMode.HTML)

    def __get_telegram_id(self, message: Message) -> str:
        return str(message.from_user.id)
