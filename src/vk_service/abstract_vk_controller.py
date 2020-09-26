from vkwave.bots import (
    SimpleLongPollUserBot
)


class AbstractVkController:
    async def welcome(self, event: SimpleLongPollUserBot) -> None:
        raise NotImplementedError

    async def help(self, event: SimpleLongPollUserBot) -> None:
        raise NotImplementedError
