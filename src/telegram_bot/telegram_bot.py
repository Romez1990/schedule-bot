from aiogram import Bot, Dispatcher
from aiogram import executor

from .greeting import Greeting
from .subscription import Subscription

from os import getenv


class TelegramBot:
    def __init__(self, subscription: Subscription, greeting: Greeting):
        bot = Bot(token=getenv('API_KEY_SCHEDULE_BOT'))
        self.dispatcher = Dispatcher(bot)
        self.dispatcher.message_handler(commands=['подписаться'])(subscription.subscribe)
        self.dispatcher.message_handler(commands=['start'])(greeting.send_welcome)
        self.dispatcher.message_handler(commands=['help'])(greeting.send_help)

    def start(self):
        executor.start_polling(self.dispatcher, skip_updates=True)

