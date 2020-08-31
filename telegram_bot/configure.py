from aiogram import Bot, Dispatcher

import logging
import os

API_TOKEN = os.getenv('API_KEY_SCHEDULE_BOT')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


