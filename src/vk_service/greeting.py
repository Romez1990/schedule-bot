from vkwave.bots import SimpleBotEvent

from src.vk_service.vk_bot import VkBot


class Greeting:
    def __init__(self, bot: VkBot):
        self.bot = bot

    async def start(self, event: SimpleBotEvent):
        await event.answer('start')

    async def help(self, event: SimpleBotEvent):
        await event.answer('help')

# bot.run_forever()
