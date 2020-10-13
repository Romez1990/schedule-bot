from aiogram import Dispatcher

from ..platform_service import PlatformService
from .telegram_bot import TelegramBot
from .telegram_controller import TelegramController


class TelegramService(PlatformService):
    def __init__(self, bot: TelegramBot, controller: TelegramController) -> None:
        self.__bot = bot
        self.__controller = controller

    async def start(self) -> None:
        self.__bot.init()
        dispatcher = self.__bot.register(Dispatcher)
        dispatcher.message_handler(commands=['start'])(self.__controller.welcome)
        dispatcher.message_handler(commands=['help'])(self.__controller.help)
        await dispatcher.skip_updates()
        await dispatcher.start_polling()
