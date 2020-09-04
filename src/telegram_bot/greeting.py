from aiogram.bot import Bot
from aiogram.types import Message
from aiogram.types import ParseMode

from .configurations.messages_text import message_text_start, message_text_help
from .configurations.button_configuration import buttons


class Greeting:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_welcome(self, message: Message) -> None:
        """
        This handler will be called when user sends `/start`
        :param message: types.Message
        :return: None
        """
        # message_text_start are taken from directory configurations/messages_text.py
        # buttons are taken from directory configurations/buttons.py
        await self.bot.send_message(message.from_user.id, message_text_start(), reply_markup=buttons,
                                    parse_mode=ParseMode.HTML)

    async def send_help(self, message: Message) -> None:
        """
        This handler will be called when user sends `/help`
        :param message: types.Message
        :return: None
        """
        # message_text_start are taken from directory configurations/messages_text.py
        # buttons are taken from directory configurations/buttons.py
        await self.bot.send_message(message.from_user.id, message_text_help(), reply_markup=buttons,
                                    parse_mode=ParseMode.HTML)
