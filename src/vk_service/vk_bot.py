from typing import (
    Optional,
)
from vkwave.bots import SimpleLongPollUserBot

from ..env import AbstractEnvironment
from .vk_controller import VkController


class VkBot:
    def __init__(self, env: AbstractEnvironment, vk_controller: VkController) -> None:
        self.__env = env
        self.__vk_controller = vk_controller
        self.__bot: Optional[SimpleLongPollUserBot] = None

    def init(self) -> None:
        token = self.__env.get_str('VK_BOT_TOKEN')
        self.__bot = SimpleLongPollUserBot(tokens=token)

    async def start(self) -> None:
        if self.__bot is None:
            self.__raise_init_error()
        self.__bot.message_handler(self.__bot.command_filter('start'))(self.__vk_controller.welcome)
        self.__bot.message_handler(self.__bot.command_filter('help'))(self.__vk_controller.help)
        await self.__bot.run_forever()

    def __raise_init_error(self) -> None:
        raise Exception('Vk bot has not been inited')