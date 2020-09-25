from vkwave.bots import SimpleLongPollUserBot
from vkwave.bots import SimpleBotEvent


class Greeting:
    def __init__(self, bot: SimpleLongPollUserBot):
        self.bot = bot

    async def start(self, event: SimpleBotEvent):
        await event.answer('start')

    async def help(self, event: SimpleBotEvent):
        await event.answer('help')

# bot.run_forever()
