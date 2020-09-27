from vkwave.bots import SimpleBotEvent

from .abstract_vk_controller import AbstractVkController


class VkController(AbstractVkController):
    async def welcome(self, event: SimpleBotEvent) -> None:
        await event.answer('')

    async def help(self, event: SimpleBotEvent) -> None:
        await event.answer('')
