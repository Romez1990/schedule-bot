from typing import (
    NoReturn,
)
from vkwave.bots import SimpleLongPollUserBot

from infrastructure.ioc_container import service
from infrastructure.config import Config
from infrastructure.errors import NoReturnError
from messenger_services.messenger_service import MessengerService
from .vk_wave_adapter import VkWaveAdapter


@service(to_self=True)
class VkWaveService(MessengerService):
    def __init__(self, config: Config) -> None:
        self.__bot = SimpleLongPollUserBot(config.vk_bot_token)
        adapter = VkWaveAdapter(self.__bot)
        super().__init__(adapter)

    async def start(self) -> NoReturn:
        await self.__bot.run(ignore_errors=False)
        raise NoReturnError
