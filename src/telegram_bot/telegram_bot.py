from aiogram import Bot, Dispatcher
from aiogram import executor

from .greeting import Greeting
from .subscription import Subscription

import logging
import os

API_TOKEN = os.getenv('API_KEY_SCHEDULE_BOT')

# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher


class TelegramBot:
    def __init__(self, subscription: Subscription, greeting: Greeting):
        bot = Bot(token=API_TOKEN)
        self.dispatcher = Dispatcher(bot)
        self.dispatcher.message_handler(commands=['подписаться'])(subscription.subscribe)
        self.dispatcher.message_handler(commands=['start'])(greeting.send_welcome)
        self.dispatcher.message_handler(commands=['help'])(greeting.send_help)

    def start(self):
        executor.start_polling(self.dispatcher, skip_updates=True)
