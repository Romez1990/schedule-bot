from aiogram import Bot
from aiogram.types import Message


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
        username = message.from_user.username
        input_from_user = message.text
        ask_theme_from_user = input_from_user.split()

        if ask_theme_from_user[1] == 'тёмная' or 'темная':
            print(f'The {username} chose a {ask_theme_from_user[1]} theme')
        elif ask_theme_from_user[1] == 'светлая' or 'белая':
            print(f'The {username} chose a {ask_theme_from_user[2]} theme')
        else:
            raise SyntaxError('Error')
