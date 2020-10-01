from aiogram import Dispatcher

from ..platform_services import PlatformService
from .telegram_bot import TelegramBot
from .telegram_controller import TelegramController


class TelegramService(PlatformService):
    def __init__(self, bot: TelegramBot, controller: TelegramController):
        self.__bot = bot
        self.__controller = controller

    async def start(self) -> None:
        """
        This function return dispatcher start
        :return: None
        """
        self.__bot.init()
        dispatcher = self.__bot.register(Dispatcher)
        dispatcher.message_handler(commands=['start'])(self.__controller.welcome)
        dispatcher.message_handler(commands=['help'])(self.__controller.help)
        await dispatcher.start_polling()
