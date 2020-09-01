from .telegram_bot.telegram_bot import TelegramBot
from .telegram_bot.subscription import Subscription

subscription = Subscription()
telegram_bot = TelegramBot(subscription)

telegram_bot.start()
