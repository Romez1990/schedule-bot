from typing import (
    NoReturn,
)
from vkbottle import Bot

from infrastructure.ioc_container import service
from infrastructure.config import Config
from infrastructure.errors import NoReturnError
from data.serializers import JsonSerializer
from messenger_services.messenger_service import (
    MessengerService,
    PayloadSerializer,
)
from .vk_adapter import VkAdapter
from .vk_keyboard_adapter import VkKeyboardAdapter
from .vk_filter_adapter import VkFilterAdapter


@service(to_self=True)
class VkService(MessengerService):
    def __init__(
            self,
            config: Config,
            keyboard_adapter: VkKeyboardAdapter,
            filter_adapter: VkFilterAdapter,
            payload_serializer: PayloadSerializer,
            json_serializer: JsonSerializer,
    ) -> None:
        self.__bot = Bot(config.vk_bot_token)
        adapter = VkAdapter(
            self.__bot,
            keyboard_adapter,
            filter_adapter,
            payload_serializer,
            json_serializer,
        )
        super().__init__(adapter)

    async def start(self) -> NoReturn:
        await self.__bot.run_polling()
        raise NoReturnError
