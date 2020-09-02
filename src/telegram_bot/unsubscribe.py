from aiogram import Bot
from aiogram.types import Message


class Unsubscribe:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def unsubscribe(self, message: Message) -> None:
        """
        This method will be called when user write `/отписаться [Название_группы
        :param message:
        :return: None
        """
        username = message.from_user.username
        group_input_from_user = message.text

        user_group = group_input_from_user.split()

