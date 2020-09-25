from vkwave.bots import simple_user_message_handler

from .vk_bot import VkBot
from .greeting import Greeting
from .subscription import Subscription


class VkDispatcher:
    def __init__(self, bot: VkBot, greeting: Greeting, subscription: Subscription):
        self.bot = bot,
        self.greeting = greeting,
        self.subscription = subscription
        self.dispatcher = simple_user_message_handler(router=bot)

    async def start(self):
        await self.dispatcher.start
