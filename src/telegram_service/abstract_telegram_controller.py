from aiogram.types import (
    Message,
)


class AbstractTelegramController:
    async def welcome(self, message: Message) -> None:
        raise NotImplementedError

    async def help(self, message: Message) -> None:
        raise NotImplementedError