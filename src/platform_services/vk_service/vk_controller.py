from vkwave.bots import SimpleBotEvent

from .vk_bot import VkBot


class VkController:
    def __init__(self, bot: VkBot):
        self.__bot = bot

    async def welcome(self, event: SimpleBotEvent) -> None:
        await event.answer('welcome')

    async def help(self, event: SimpleBotEvent) -> None:
        await event.answer('help')
