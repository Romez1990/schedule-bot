from .abstract_telegram_controller import AbstractTelegramController
from .telegram_bot import TelegramBot


class TelegramController(AbstractTelegramController):
    def __init__(self, bot: TelegramBot) -> None:
        self.__bot = bot
