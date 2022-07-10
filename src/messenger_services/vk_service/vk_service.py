from typing import (
    NoReturn,
)
from vkbottle import Bot

from infrastructure.ioc_container import service
from infrastructure.config import Config
from infrastructure.errors import NoReturnError
from messenger_services.messenger_service import MessengerService
from .vk_adapter import VkAdapter
from .vk_keyboard_adapter import VkKeyboardAdapter


@service(to_self=True)
class VkService(MessengerService):
    def __init__(
            self,
            config: Config,
            keyboard_adapter: VkKeyboardAdapter,
    ) -> None:
        self.__bot = Bot(config.vk_bot_token)
        adapter = VkAdapter(
            self.__bot,
            keyboard_adapter,
        )
        super().__init__(adapter)

    async def start(self) -> NoReturn:
        await self.__bot.run_polling()
        raise NoReturnError
