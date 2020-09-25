from vkwave.bots import SimpleLongPollBot

bot = SimpleLongPollBot(tokens="d3a83eb6b7c23bf02582bd23281b23702190692175bcdc36bd3171c39e53768c07e0a4a3c14ea28322ba6",
                        group_id=196098913)


@bot.message_handler(bot.text_filter("bye"))
def handle(_) -> str:
    return "bye world"


@bot.message_handler(bot.text_filter("hello"))
async def handle(event: bot.SimpleBotEvent):
    await event.answer("hello world!")


bot.run_forever()
