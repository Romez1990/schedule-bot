from aiogram import Dispatcher

from .abstract_telegram_dispatcher import AbstractTelegramDispatcher
from .abstract_telegram_bot import AbstractTelegramBot
from .abstract_telegram_controller import AbstractTelegramController


class TelegramDispatcher(AbstractTelegramDispatcher):
    def __init__(self, bot: AbstractTelegramBot, controller: AbstractTelegramController) -> None:
        self.__dispatcher = bot.register_bot(Dispatcher)
        self.__dispatcher.message_handler(commands=['start'])(controller.welcome)
        self.__dispatcher.message_handler(commands=['help'])(controller.help)

    async def start(self) -> None:
        """
        This function launches the bot
        :return: None
        """
        await self.__dispatcher.start_polling()
