from aiogram import Dispatcher, Bot
from aiogram.utils import executor

from .greeting import Greeting
from .subscription import Subscription


class TelegramDispatcher:
    def __init__(self, bot: Bot, subscription: Subscription, greeting: Greeting):
        self.dispatcher = Dispatcher(bot)
        self.dispatcher.message_handler(commands=['подписаться'])(subscription.subscribe)
        self.dispatcher.message_handler(commands=['start'])(greeting.send_welcome)
        self.dispatcher.message_handler(commands=['help'])(greeting.send_help)

    def start(self) -> None:
        executor.start_polling(self.dispatcher, skip_updates=True)
