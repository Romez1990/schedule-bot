from aiogram import Bot, Dispatcher

from infrastructure.ioc_container import service
from infrastructure.config import Config
from messenger_services.messenger_service import MessengerService
from .telegram_adapter import TelegramAdapter


@service(to_self=True)
class TelegramService(MessengerService):
    def __init__(self, config: Config) -> None:
        bot = Bot(config.telegram_bot_token)
        self.__dispatcher = Dispatcher(bot)
        adapter = TelegramAdapter(bot, self.__dispatcher)
        super().__init__(adapter)

    async def start(self) -> None:
        await self.__dispatcher.skip_updates()
        await self.__dispatcher.start_polling()