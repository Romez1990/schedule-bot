from threading import Thread
from typing import List
from time import sleep
from datetime import datetime
from os import getenv as env
from dotenv import load_dotenv
from vk_api import VkApi, VkUpload
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from io import BytesIO
from asyncio import run
from scraper import Scraper
from renderer import Renderer
from structures import Group, Schedule

from dbtest import User, UserGroup, GroupHash, Service, Theme, Mode, DBHelper

load_dotenv()

vk_session = VkApi(token=env('VK_BOT_TOKEN'))
longpoll = VkBotLongPoll(vk_session, '195862525')

schedule: Schedule
renderer = Renderer()


async def fetch_schedule() -> None:
    scraper = Scraper()
    global schedule
    schedule = await scraper.fetch_schedule()


def is_group_exist(group_name: str) -> bool:
    groups = schedule.groups
    return any(group_name.lower() == str(group).lower() for group in groups)


def build_keyboard(user: User) -> VkKeyboard:
    theme = user.theme
    mode = user.mode

    light_button = VkKeyboardColor.PRIMARY if theme == Theme.LIGHT else VkKeyboardColor.SECONDARY
    dark_button = VkKeyboardColor.PRIMARY if theme == Theme.DARK else VkKeyboardColor.SECONDARY
    manual_button = VkKeyboardColor.PRIMARY if mode == Mode.MANUAL else VkKeyboardColor.SECONDARY
    auto_button = VkKeyboardColor.PRIMARY if mode == Mode.AUTOMATIC else VkKeyboardColor.SECONDARY

    keyboard = VkKeyboard(one_time=True)
    keyboard.add_button('Расписание', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()  # Переход на вторую строку
    keyboard.add_button('Тема Светлая', light_button)
    keyboard.add_button('Тема Тёмная', dark_button)
    keyboard.add_line()  # Переход на третью строку
    keyboard.add_button('Режим Ручной', manual_button)
    keyboard.add_button('Режим Автоматический', auto_button)

    return keyboard


def send_message(user_id: int, user: User, message: str):
    keyboard = build_keyboard(user)
    vk_session.method('messages.send', {'user_id': user_id, 'random_id': get_random_id(), 'message': message, 'keyboard': keyboard.get_keyboard()})


def send_picture(user_id: int, user: User, message: str, picture_bytes: BytesIO):
    keyboard = build_keyboard(user)
    attachments = []
    upload = VkUpload(vk_session)
    photo = upload.photo_messages(photos=picture_bytes)[0]
    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
    vk_session.method('messages.send', {'user_id': user_id, 'random_id': get_random_id(), 'message': message, 'keyboard': keyboard.get_keyboard(), 'attachment': ','.join(attachments)})


def parse_commands(user_id: int, message: str):
    data = message
    if data == 'Начать':
        if not DBHelper.is_user_presented(user_id):
            DBHelper.add_user(user_id, Service.VK, Mode.MANUAL, Theme.LIGHT)
            send_message(user_id, DBHelper.get_user(user_id), 'Добро пожаловать в бот расписания!')
        else:
            send_message(user_id, DBHelper.get_user(user_id), 'Добро пожаловать в бот расписания!')

    user_g = DBHelper.get_user(user_id)

    _group = 'Группа '
    if data == 'Группа':
        send_message(user_id, user_g, 'Использование: Группа [ИМЯ_ГРУППЫ]')
    elif data[:len(_group)] == _group:
        data = data[len(_group):]
        if is_group_exist(data):
            if DBHelper.is_user_presented(user_id):
                user = DBHelper.get_user(user_id)
                if DBHelper.is_group_presented_on_user(user, data):
                    DBHelper.del_group_from_user(user, data)
                    send_message(user_id, user, f'Вы отписались от расписания группы {data}')
                else:
                    DBHelper.add_group_to_user(user, data)
                    send_message(user_id, user, f'Вы подписались на расписание группы {data}')
        else:
            send_message(user_id, user_g, f'Группа {data} не существует, либо в настоящее время не представлена в расписании')

    _schedule = 'Расписание '
    if data == 'Расписание':  # +таймаут
        if DBHelper.is_user_presented(user_id):
            user = DBHelper.get_user(user_id)
            user_groups = DBHelper.get_groups_from_user(user)
            if len(user_groups) > 0:
                user_schedule = schedule.filter(user_groups)
                schedule_photo = renderer.render(user_schedule, user.theme.name.lower())
                send_picture(user_id, user, f'Расписание для групп {", ".join(str(g) for g in user_groups)}', schedule_photo)
            else:
                send_message(user_id, user, 'Вы не подписаны ни на одну группу')
    elif data[:len(_schedule)] == _schedule:
        data = data[len(_schedule):]
        if is_group_exist(data):
            if DBHelper.is_user_presented(user_id):
                user = DBHelper.get_user(user_id)
                user_schedule = schedule.filter([Group(data)])
                schedule_photo = renderer.render(user_schedule, user.theme.name.lower())
                send_picture(user_id, user, f'Расписание для группы {data}', schedule_photo)
        else:
            send_message(user_id, user_g, f'Группа {data} не существует, либо в настоящее время не представлена в расписании')

    _theme = 'Тема '
    if data == 'Тема':
        send_message(user_id, user_g, 'Использование: Тема Светлая/Тёмная')
    elif data[:len(_theme)] == _theme:
        data = data[len(_theme):].lower()
        if DBHelper.is_user_presented(user_id):
            user = DBHelper.get_user(user_id)
            if data == 'светлая':
                user.theme = Theme.LIGHT
                DBHelper.update()
                send_message(user_id, user, f'Светлая цветовая схема была установлена')
            elif data == 'тёмная':
                user.theme = Theme.DARK
                DBHelper.update()
                send_message(user_id, user, f'Тёмная цветовая схема была установлена')
            else:
                send_message(user_id, user, f'Цветовая схема не найдена\nИспользование: Тема Светлая/Тёмная')

    _mode = 'Режим '
    if data == 'Режим':
        send_message(user_id, user_g, 'Использование: Режим Ручной/Автоматический')
    elif data[:len(_mode)] == _mode:
        data = data[len(_mode):].lower()
        if DBHelper.is_user_presented(user_id):
            user = DBHelper.get_user(user_id)
            if data == 'ручной':
                user.mode = Mode.MANUAL
                DBHelper.update()
                send_message(user_id, user, f'Ручной режим был установлен')
            elif data == 'автоматический':
                user.mode = Mode.AUTOMATIC
                DBHelper.update()
                send_message(user_id, user, f'Автоматический режим был установлен')
            else:
                send_message(user_id, user, f'Данного режима не существует\nИспользование: Режим Ручной/Автоматический')


def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW and event.message.text:
            user_id = event.message.from_id
            user_text = event.message.text

            parse_commands(user_id, user_text)

            print(f'Новое сообщение:\nДля меня от: {user_id}\nТекст: {user_text}\n')


def update():
    while True:
        print(f'[{datetime.now().time()}] update started')

        run(fetch_schedule())

        groups_to_send: List[str] = []  # массив групп для отправки
        users_sent: List[int] = []

        schedule_groups = schedule.groups  # взять список групп из полученного расписания
        for _group in schedule_groups:  # цикл для списка групп:
            group_name = str(_group)
            # print(group_name)  # INFO: DEBUG
            if not DBHelper.is_group_presented_in_hashtable(group_name):  # если группы нет в GroupHashes
                DBHelper.add_group_to_hashtable(group_name, 0, 0)  # добавить ее

            group_hash = DBHelper.get_group_hashes(group_name)
            cur_hash = hash(schedule[Group(group_name)])  # make_hash(group)  # высчитать хэш расписания

            if group_hash.old_hash == 0:  # если старый хэш не существует
                group_hash.old_hash = cur_hash  # старый занести в базу
                group_hash.cur_hash = cur_hash  # новый занести в базу
                DBHelper.update()  # отправить изменения
                continue  # пропустить следующий шаг

            if cur_hash != group_hash.old_hash:  # если новый хэш не соответствует старому
                group_hash.old_hash = cur_hash  # обновляем старый хэш
                if group_name not in groups_to_send:  # если группа не в массиве A
                    groups_to_send.append(group_name)  # записываем ее туда

            DBHelper.update()

        print(f'[{datetime.now().time()}] update finished')
        if groups_to_send:
            print(groups_to_send)

        for _group in groups_to_send:  # цикл для массива A
            users_ids = DBHelper.get_users_with_group(_group)  # получить всех пользователей с группой
            print(users_ids)
            if users_ids:  # если пользователи есть
                for user_id in users_ids:  # цикл для списка пользователей
                    if user_id.user_id in users_sent:  # если юзеру уже было отправлено расписание
                        continue  # пропускаем

                    user = DBHelper.get_user_by_id(user_id.user_id)  # получаем пользователя
                    if user.mode == Mode.MANUAL:  # если у пользователя режим ручной
                        continue  # пропускаем

                    print(f'sending to {user.user_id}')

                    user_groups = DBHelper.get_groups_from_user(user)  # берем список групп у пользователя
                    if len(user_groups) > 0:
                        user_schedule = schedule.filter(user_groups)  # фильтруем
                        schedule_photo = renderer.render(user_schedule, user.theme.name.lower())  # рендерим
                        send_picture(user.user_id, user, f'Расписание для групп {", ".join(str(g) for g in user_groups)}', schedule_photo)  # отправляем
                        users_sent.append(user_id.user_id)

        groups_to_send.clear()
        users_sent.clear()

        sleep(1800)  # сон 30 минут


if __name__ == '__main__':
    # run(fetch_schedule())
    # groups = schedule.groups
    # for group in groups:
    #     name = str(group)
    #     sched = schedule[Group(name)]
    #     print(f'{name} {hash(sched)}')

    update_thread = Thread(target=update)
    bot_thread = Thread(target=main)
    update_thread.start()
    bot_thread.start()
