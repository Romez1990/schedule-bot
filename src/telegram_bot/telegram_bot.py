from aiogram import Bot, Dispatcher
from aiogram import executor, types
from .subscription import Subscription
import logging
import os

API_TOKEN = os.getenv('API_KEY_SCHEDULE_BOT')

# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher


class TelegramBot:
    def __init__(self, subscription: Subscription):
        bot = Bot(token=API_TOKEN)
        self.dispatcher = Dispatcher(bot)
        self.dispatcher.message_handler(commands=['подписаться'])(subscription.subscribe)

    def start(self):
        executor.start_polling(self.dispatcher, skip_updates=True)
