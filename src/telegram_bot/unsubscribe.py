from aiogram import Bot
from aiogram.types import Message


class Unsubscribe:
    def __init__(self, bot: Bot):
        self.bot = bot

    def unsubscribe(self, message: Message) -> None:
        """
        This method will be called when user write `/отписаться [Название_группы
        :param message:
        :return: None
        """
        pass
