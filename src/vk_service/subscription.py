from vkwave.bots import SimpleBotEvent

from .vk_bot import VkBot


class Subscription:
    def __init__(self, bot: VkBot):
        self.bot = bot

    async def subscribe(self, event: SimpleBotEvent):
        await event.answer('Вы подписались')

    async def unsubscribe(self, event: SimpleBotEvent):
        await event.answer('Вы отписались')

    async def check(self, event: SimpleBotEvent):
        await event.answer('Вы проверили')
