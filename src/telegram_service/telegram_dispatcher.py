from aiogram import Dispatcher, Bot

from .abstract_telegram_dispatcher import AbstractTelegramDispatcher
from .telegram_bot import TelegramBot
from .greeting import Greeting
from .subscription import Subscription
from .theme_decoration import ThemeDecoration


class TelegramDispatcher(AbstractTelegramDispatcher):
    def __init__(self, bot: TelegramBot, subscription: Subscription, greeting: Greeting,
                 theme_decoration: ThemeDecoration) -> None:
        self.__dispatcher = bot.register_bot(Dispatcher)
        self.__dispatcher.message_handler(commands=['подписаться'])(subscription.subscribe)
        self.__dispatcher.message_handler(commands=['отписаться'])(subscription.unsubscribe)
        self.__dispatcher.message_handler(commands=['изменить'])(subscription.change)
        self.__dispatcher.message_handler(commands=['start'])(greeting.send_welcome)
        self.__dispatcher.message_handler(commands=['help'])(greeting.send_help)
        self.__dispatcher.message_handler(commands=['тема'])(theme_decoration.ask_theme)

    async def start(self) -> None:
        """
        This function launches the bot
        :return: None
        """
        await self.__dispatcher.start_polling()
