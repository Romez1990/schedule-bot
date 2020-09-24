from typing import (
    Callable,
    TypeVar,
)

from aiogram import Bot

from ..env import AbstractEnvironment

T = TypeVar('T')


class TelegramBot:
    def __init__(self, env: AbstractEnvironment):
        token = env.get_str('TELEGRAM_BOT_TOKEN')
        self.__bot = Bot(token=token)

    def register_bot(self, func: Callable[[Bot], T]) -> T:
        return func(self.__bot)
