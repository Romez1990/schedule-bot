from vkwave.bots import SimpleLongPollUserBot

from infrastructure.config import Config
from infrastructure.ioc_container import service
from messenger_services.messenger_service import MessengerService
from .vk_wave_adapter import VkWaveAdapter


@service(to_self=True)
class VkWaveService(MessengerService):
    def __init__(self, config: Config) -> None:
        self.__bot = SimpleLongPollUserBot(config.vk_bot_token)
        adapter = VkWaveAdapter(self.__bot)
        super().__init__(adapter)

    async def start(self) -> None:
        await self.__bot.run(ignore_errors=False)
