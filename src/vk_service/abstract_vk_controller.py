from vkwave.bots import (
    SimpleBotEvent,
)


class AbstractVkController:
    async def welcome(self, event: SimpleBotEvent) -> None:
        raise NotImplementedError

    async def help(self, event: SimpleBotEvent) -> None:
        raise NotImplementedError
