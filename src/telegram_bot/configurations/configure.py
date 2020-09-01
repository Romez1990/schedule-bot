from aiogram import Bot, Dispatcher

import logging
import os

API_TOKEN = os.getenv('API_KEY_SCHEDULE_BOT')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

"""
Here I will import all dependencies

Короче, тут буду брать все переменные что бы не писать все время Bot и к нему API добавлять, думаю не говнокод

p.s Впервые в жизни такие комментарии пишу xDD
"""
