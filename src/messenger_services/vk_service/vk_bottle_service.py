from typing import (
    NoReturn,
)
from vkbottle import Bot

from infrastructure.ioc_container import service
from infrastructure.config import Config
from infrastructure.errors import NoReturnError
from messenger_services.messenger_service import MessengerService
from .vk_bottle_adapter import VkBottleAdapter


@service(to_self=True)
class VkBottleService(MessengerService):
    def __init__(self, config: Config) -> None:
        self.__bot = Bot(config.vk_bot_token)
        adapter = VkBottleAdapter(self.__bot)
        super().__init__(adapter)

    async def start(self) -> NoReturn:
        await self.__bot.run_polling()
        raise NoReturnError
