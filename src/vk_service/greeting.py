from vkwave.bots import SimpleLongPollUserBot

bot = SimpleLongPollUserBot(
    tokens="d3a83eb6b7c23bf02582bd23281b23702190692175bcdc36bd3171c39e53768c07e0a4a3c14ea28322ba6", )


@bot.message_handler(bot.command_filter('start'))
async def start(event: bot.SimpleBotEvent):
    await event.answer('start')


@bot.message_handler(bot.command_filter('help'))
async def help(event: bot.SimpleBotEvent):
    await event.answer('help')


bot.run_forever()
