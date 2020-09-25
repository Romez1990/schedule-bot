from aiogram.types import (
    Message,
)

from ..bot_services import (
    AbstractUserService,
    AbstractUserSettingsService,
    AbstractSubscriptionService,
)
from .abstract_telegram_controller import AbstractTelegramController
from .telegram_bot import TelegramBot


class TelegramController(AbstractTelegramController):
    def __init__(
            self,
            bot: TelegramBot,
            user_service: AbstractUserService,
            user_settings_service: AbstractUserSettingsService,
            subscription_service: AbstractSubscriptionService,
    ) -> None:
        self.__bot = bot
        self.__user_service = user_service
        self.__user_settings_service = user_settings_service
        self.__subscription_service = subscription_service
        self.__platform = 'telegram'

    def __get_telegram_id(self, message: Message) -> str:
        return str(message.from_user.id)
