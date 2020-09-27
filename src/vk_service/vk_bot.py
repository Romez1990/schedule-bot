from vkwave.bots import SimpleLongPollUserBot

from ..env import AbstractEnvironment
from .vk_controller import VkController


class VkBot:
    def __init__(self, env: AbstractEnvironment, vk_controller: VkController) -> None:
        token = env.get_str('VK_BOT_TOKEN')
        self.__bot = SimpleLongPollUserBot(tokens=token)
        self.__bot.message_handler(self.__bot.command_filter('start'))(vk_controller.welcome)
        self.__bot.message_handler(self.__bot.command_filter('help'))(vk_controller.help)

    async def start(self) -> None:
        await self.__bot.run_forever()
