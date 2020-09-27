from vkwave.bots import SimpleBotEvent


class VkController:
    async def welcome(self, event: SimpleBotEvent) -> None:
        await event.answer('')

    async def help(self, event: SimpleBotEvent) -> None:
        await event.answer('')
