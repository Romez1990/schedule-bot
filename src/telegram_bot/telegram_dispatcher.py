from aiogram import Dispatcher, Bot
from aiogram.utils import executor

from .greeting import Greeting
from .subscription import Subscription
from .unsubscribe import Unsubscribe
from .theme_decoration import ThemeDecoration


class TelegramDispatcher:
    def __init__(self, bot: Bot, subscription: Subscription, greeting: Greeting, unsubscribe: Unsubscribe,
                 theme_decoration: ThemeDecoration):
        self.dispatcher = Dispatcher(bot)
        self.dispatcher.message_handler(commands=['подписаться'])(subscription.subscribe)
        self.dispatcher.message_handler(commands=['start'])(greeting.send_welcome)
        self.dispatcher.message_handler(commands=['help'])(greeting.send_help)
        self.dispatcher.message_handler(commands=['отписаться'])(unsubscribe.unsubscribe)
        self.dispatcher.message_handler(commands=['тема'])(theme_decoration.ask_theme)

    def start(self) -> None:
        """
        This function launches the bot
        :return: None
        """
        executor.start_polling(self.dispatcher, skip_updates=True)
