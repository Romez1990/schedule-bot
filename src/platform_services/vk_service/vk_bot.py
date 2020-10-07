from typing import (
    Optional,
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
        self.__bot: Optional[SimpleLongPollUserBot] = None

    def init(self) -> None:
        token = self.__env.get_str('VK_BOT_TOKEN')
        self.__bot = SimpleLongPollUserBot(tokens=token)

    def message_handler(self, *filters: BaseFilter) -> Callable:
        if self.__bot is None:
            self.__raise_init_error()
        return self.__bot.message_handler(*filters)

    def command_filter(self, commands: str,
                       prefixes: Tuple[str, ...] = ("/", "!"),
                       ignore_case: bool = True) -> CommandsFilter:
        if self.__bot is None:
            self.__raise_init_error()
        return self.__bot.command_filter(commands, prefixes, ignore_case)

    async def start(self) -> None:
        if self.__bot is None:
            self.__raise_init_error()
        await self.__bot.run()

    def __raise_init_error(self) -> None:
        raise Exception('Vk bot has not been inited')
