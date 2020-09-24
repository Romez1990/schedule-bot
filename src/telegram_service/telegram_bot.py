from aiogram import Bot

from os import getenv


class TelegramBot:
    def __init__(self):
        self.__bot = Bot(token=getenv('API_KEY_SCHEDULE_BOT'))

    @property
    def bot(self) -> Bot:
        """
        This property function return bot
        :return: Bot
        """
        return self.__bot
