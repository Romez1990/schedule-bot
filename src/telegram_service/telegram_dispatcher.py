from aiogram import Dispatcher

from .telegram_bot import TelegramBot
from .telegram_controller import TelegramController


class TelegramDispatcher:
    def __init__(self, bot: TelegramBot, controller: TelegramController) -> None:
        self.__dispatcher = bot.register_bot(Dispatcher)
        self.__dispatcher.message_handler(commands=['start'])(controller.welcome)
        self.__dispatcher.message_handler(commands=['help'])(controller.help)

    async def start(self) -> None:
        """
        This function launches the bot
        :return: None
        """
        await self.__dispatcher.start_polling()
