from typing import (
    Callable,
    Union,
    TypeVar,
)
from aiogram import Bot
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    ForceReply,
)

from ..env import AbstractEnvironment

T = TypeVar('T')


class TelegramBot:
    def __init__(self, env: AbstractEnvironment):
        token = env.get_str('TELEGRAM_BOT_TOKEN')
        self.__bot = Bot(token=token)

    def register_bot(self, func: Callable[[Bot], T]) -> T:
        return func(self.__bot)

    async def send_message(self, chat_id: str, text: str, *, parse_mode: str = None,
                           disable_web_page_preview: bool = None, disable_notification: bool = None,
                           reply_to_message_id: int = None,
                           reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                                               ForceReply] = None) -> Message:
        return await self.__bot.send_message(chat_id, text, parse_mode, disable_web_page_preview, disable_notification,
                                             reply_to_message_id, reply_markup)
