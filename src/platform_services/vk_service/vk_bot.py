from typing import (
    Tuple,
    Callable,
)
from vkwave.bots import (
    SimpleLongPollUserBot,
    CommandsFilter,
)
from vkwave.bots.core import (
    BaseFilter,
)

from src.env import EnvironmentInterface


class VkBot:
    def __init__(self, env: EnvironmentInterface) -> None:
        self.__env = env

    __bot: SimpleLongPollUserBot

    def init(self) -> None:
        token = self.__env.get_str('VK_BOT_TOKEN')
        self.__bot = SimpleLongPollUserBot(tokens=token)

    def message_handler(self, *filters: BaseFilter) -> Callable:
        return self.__bot.message_handler(*filters)

    def command_filter(self, commands: str,
                       prefixes: Tuple[str, ...] = ("/", "!"),
                       ignore_case: bool = True) -> CommandsFilter:
        return self.__bot.command_filter(commands, prefixes, ignore_case)

    async def start(self) -> None:
        await self.__bot.run()
