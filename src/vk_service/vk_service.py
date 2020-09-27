from .vk_bot import VkBot
from .vk_controller import VkController
from ..platform_service import PlatformService


class VkService(PlatformService):
    def __init__(self, bot: VkBot, controller: VkController) -> None:  # Change dispatcher type change to another
        self.__bot = bot
        self.__controller = controller

    async def start(self) -> None:
        self.__bot.init()


