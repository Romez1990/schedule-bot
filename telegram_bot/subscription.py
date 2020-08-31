from aiogram import executor, types
from telegram_bot.configurations.configure import dp
from telegram_bot.configurations.messages_text import message_text_start, message_text_help
from telegram_bot.configurations.button_configuration import buttons
from aiogram.types import ParseMode

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

