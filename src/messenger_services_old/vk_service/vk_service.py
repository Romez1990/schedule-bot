from ..platform_service import PlatformService
from .vk_bot import VkBot
from .vk_controller import VkController


class VkService(PlatformService):
    def __init__(self, bot: VkBot, controller: VkController) -> None:
        self.__bot = bot
        self.__controller = controller

    async def start(self) -> None:
        self.__bot.init()
        self.__bot.message_handler(self.__bot.command_filter('start'))(self.__controller.welcome)
        self.__bot.message_handler(self.__bot.command_filter('help'))(self.__controller.help)
        await self.__bot.start()
