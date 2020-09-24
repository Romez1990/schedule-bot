from aiogram import Bot

from ..env import AbstractEnvironment


class TelegramBot:
    def __init__(self, env: AbstractEnvironment):
        token = env.get_str('API_KEY_SCHEDULE_BOT')
        self.__bot = Bot(token=token)

    @property
    def bot(self) -> Bot:
        """
        This property function return bot
        :return: Bot
        """
        return self.__bot
