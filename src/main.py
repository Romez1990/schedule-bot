from .telegram_bot.telegram_bot import TelegramBot
from .telegram_bot.subscription import Subscription
from .telegram_bot.greeting import Greeting

subscription = Subscription()
greeting = Greeting()
telegram_bot = TelegramBot(subscription, greeting)

telegram_bot.start()
