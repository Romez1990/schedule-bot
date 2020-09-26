from aiogram.types import (
    Message,
    ParseMode,
)

from ..bot_services import (
    AbstractUserService,
    AbstractUserSettingsService,
    AbstractSubscriptionService,
)
from .abstract_telegram_controller import AbstractTelegramController
from .abstract_telegram_bot import AbstractTelegramBot
from .configurations.messages_text import message_text_start, message_text_help
from .configurations.button_configuration import buttons


class TelegramController(AbstractTelegramController):
    def __init__(
            self,
            bot: AbstractTelegramBot,
            user_service: AbstractUserService,
            user_settings_service: AbstractUserSettingsService,
            subscription_service: AbstractSubscriptionService,
    ) -> None:
        self.__bot = bot
        self.__user_service = user_service
        self.__user_settings_service = user_settings_service
        self.__subscription_service = subscription_service
        self.__platform = 'telegram'

    async def welcome(self, message: Message) -> None:
        telegram_id = self.__get_telegram_id(message)
        await self.__user_service.create_if_not_exists(self.__platform, telegram_id)
        await self.__bot.send_message(telegram_id, message_text_start(),
                                      reply_markup=buttons, parse_mode=ParseMode.HTML)

    async def help(self, message: Message) -> None:
        telegram_id = self.__get_telegram_id(message)
        await self.__bot.send_message(telegram_id, message_text_help(),
                                      reply_markup=buttons, parse_mode=ParseMode.HTML)

    def __get_telegram_id(self, message: Message) -> str:
        return str(message.from_user.id)
