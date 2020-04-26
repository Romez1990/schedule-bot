from os import getenv as env
from dotenv import load_dotenv
from telebot import AsyncTeleBot
from telebot.types import Message

from asyncio import run
# from asyncio import sleep
from io import BytesIO

from scraper import Scraper
from renderer import Renderer
from structures import Group, Schedule

# from telebot import apihelper
# apihelper.proxy = {'http':'http://10.10.1.10:3128'}

load_dotenv()

bot = AsyncTeleBot(env('BOT_TOKEN'))

schedule: Schedule


async def schedule_fetch_thread() -> None:
    scraper = Scraper()
    global schedule
    schedule = await scraper.fetch_schedule()


# - запрос /start - создание пользователя, если нет в базе
# - запрос /groups <string> - задание групп, расписания которых будут отправлены пользователю
# - запрос /theme <string> - задание цветовой темы расписания
# - запрос /mode <int> - режим работы (0 - ручной, 1 - оповещение об изменениях, 2 - информация на текущий день с утра, 3 - информация на следующий день с вечера)
# - запрос /get <opt:string> - отправить расписание заданных групп или если введена строка, то отправить расписание определенной группы
# bot.send_message(message.chat.id, "Доступные команды:\n"
#                                   "/get <группа> - отправить нанана/отправить расписание выбранной группы\n"
#                                   "/groups <группы> - указать группы, расписания для которых будут отправлены пользователю (вводить через пробел)\n"
#                                   "/theme <>\n")

@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    # bot.send_message(message.chat.id, "4ПрИн")
    # bot.send_photo(message.chat.id, light_schedule)
    # bot.send_photo(message.chat.id, dark_schedule)
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['theme'])
def set_theme(message: Message):
    text = message.text


@bot.message_handler(commands=['mode'])
def set_mode(message: Message):
    text = message.text


@bot.message_handler(commands=['groups'])
def set_groups(message: Message):
    text = message.text


@bot.message_handler(commands=['schedule'])
def send_schedule(message: Message):
    message.chat.id
    text: str = message.text
    # todo: add ~10sec check to prevent DOS
    if text == "/schedule":  # send schedule for 'groups'
        bot.send_message(message.chat.id, text)
        groups = schedule.filter([
            Group('4ПрИн-5.16'),
            Group('4ПрИн-5а.16'),
        ])

        renderer = Renderer()
        light_schedule = renderer.render(groups, 'light')
        dark_schedule = renderer.render(groups, 'dark')
        # todo: 1) read 'groups' from DB; 2) get schedule for specified groups; 3) send them here
    else:  # send schedule for specified group
        text = text.lstrip('/schedule ')
        bot.send_message(message.chat.id, text)
        # todo: 1) get schedule for specified group; 2) send it

# @bot.message_handler(func=lambda message: True)
# def echo_all(message: Message):
#     bot.reply_to(message, message.text)


run(schedule_fetch_thread())
bot.polling()











# import telegram
# from telegram import ChatAction, ReplyKeyboardMarkup
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
#
# from asyncio import run
# from io import BytesIO
#
# from scraper import Scraper
# from renderer import Renderer
# from structures import Group
#
#
# async def test(bot, context) -> None:
#     scraper = Scraper()
#     schedule = await scraper.fetch_schedule()
#     my_group = schedule.filter([
#         Group('4ПрИн-5.16'),
#         Group('4ПрИн-5а.16'),
#     ])
#
#     renderer = Renderer()
#     light_schedule = renderer.render(my_group, 'light')
#     dark_schedule = renderer.render(my_group, 'dark')
#
#     bot.send_photo(bot.message.chat_id, dark_schedule)
#     bot.message.reply_text()
#
# def hello(bot, context):
#     bot.message.reply_text(
#         'Hello {}'.format(bot.message.from_user.first_name))
#
#
# updater = Updater('843363463:AAEujcL4klciO0z9MjDt-RfDxTCh5TaOqvw', use_context=True)
#
# updater.dispatcher.add_handler(CommandHandler('hello', hello))
#
# updater.start_polling()
# updater.idle()
