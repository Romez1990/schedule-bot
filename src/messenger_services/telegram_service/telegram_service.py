from typing import (
    NoReturn,
)
from aiogram import Bot, Dispatcher

from infrastructure.ioc_container import service
from infrastructure.config import Config
from infrastructure.errors import NoReturnError
from messenger_services.messenger_service import MessengerService
from .telegram_adapter import TelegramAdapter
from .telegram_keyboard_adapter import TelegramKeyboardAdapter


@service(to_self=True)
class TelegramService(MessengerService):
    def __init__(self, config: Config, keyboard_adapter: TelegramKeyboardAdapter) -> None:
        bot = Bot(config.telegram_bot_token)
        self.__dispatcher = Dispatcher(bot)
        adapter = TelegramAdapter(bot, self.__dispatcher, keyboard_adapter)
        super().__init__(adapter)

    async def start(self) -> NoReturn:
        await self.__dispatcher.skip_updates()
        await self.__dispatcher.start_polling()
        raise NoReturnError
