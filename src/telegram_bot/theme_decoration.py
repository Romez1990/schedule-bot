from aiogram import Bot
from aiogram.types import Message
from aiogram.types import ParseMode

from .configurations.messages_text import message_theme


class ThemeDecoration:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def theme(self, theme: bool, username: str) -> None:
        """
        We will call this function at the bottom, and it will send the necessary requests to the database.
        :param theme:
        :param username:
        :return: None
        """
        pass

    async def ask_theme(self, message: Message) -> None:
        """
        This method will be called when the user selects a theme
        :param message:
        :return: None
        """

        theme = [mess for mess in message.text.split()][1]

        if theme == 'тёмная' or 'темная':
            await self.bot.send_message(message.from_user.id, message_theme(theme),
                                        parse_mode=ParseMode.HTML)
        elif theme == 'светлая' or 'белая':
            await self.bot.send_message(message.from_user.id, message_theme(theme),
                                        parse_mode=ParseMode.HTML)
        else:
            raise SyntaxError('Error')
