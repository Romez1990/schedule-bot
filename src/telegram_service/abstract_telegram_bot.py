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

T = TypeVar('T')


class AbstractTelegramBot:
    def register_bot(self, func: Callable[[Bot], T]) -> T:
        raise NotImplementedError

    async def send_message(self, chat_id: str, text: str, *, parse_mode: str = None,
                           disable_web_page_preview: bool = None, disable_notification: bool = None,
                           reply_to_message_id: int = None,
                           reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                                               ForceReply] = None) -> Message:
        raise NotImplementedError
