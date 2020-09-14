from aiogram import Bot
from aiogram.types import Message
from aiogram.types import ParseMode

from .configurations.messages_text import message_theme
from ..services.setting_service import SettingService


class ThemeDecoration:
    def __init__(self, bot: Bot, user_settings: SettingService):
        self.bot = bot
        self.user_settings = user_settings

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
            await self.user_settings.add(user_id=7, theme=theme)  # here need worked user_id, here need work method
        elif theme == 'светлая' or 'белая':
            await self.bot.send_message(message.from_user.id, message_theme(theme),
                                        parse_mode=ParseMode.HTML)
            await self.user_settings.add(user_id=0, theme=theme)  # here need worked user_id, here need work method
        else:
            raise SyntaxError('Error')
