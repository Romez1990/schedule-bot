from aiogram import Dispatcher

from .abstract_telegram_dispatcher import AbstractTelegramDispatcher
from .telegram_bot import TelegramBot
from .abstract_telegram_controller import AbstractTelegramController


class TelegramDispatcher(AbstractTelegramDispatcher):
    def __init__(self, bot: TelegramBot, controller: AbstractTelegramController) -> None:
        self.__dispatcher = bot.register_bot(Dispatcher)
        self.__dispatcher.message_handler(commands=['start'])(controller.welcome)
        self.__dispatcher.message_handler(commands=['help'])(controller.help)

    async def start(self) -> None:
        """
        This function launches the bot
        :return: None
        """
        await self.__dispatcher.start_polling()
