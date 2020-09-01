from aiogram import Bot

from .greeting import Greeting
from .subscription import Subscription

from os import getenv


class TelegramBot:
    def __init__(self, subscription: Subscription, greeting: Greeting):
        self._bot_api = Bot(token=getenv('API_KEY_SCHEDULE_BOT'))

    @property
    def bot(self):
        return self._bot_api
