def message_text_help():
    return '''
<em>/start</em> - <strong>команда для старта бота</strong> (по умолчанию включен)\n
<em>Подписаться [Название_Группы]</em> - <strong>подписаться на рассылку расписание</strong>\n
<em>Отписаться [Название_Группы]</em> - <strong>отписаться от рассылки расписание</strong>\n
<em>Тёмная тема</em> - <strong>получаться рассылку расписание в тёмной теме</strong>\n
<em>Светлая тема</em> - <strong>получаться рассылку расписание в светвлой теме</strong>\n
        '''


def message_text_start():
    return '''
<strong>Приветствую дорогой студент👋<strike>или уже не студент</strike>\n
🦾Я бот позволяющее предоставить тебе расписание твоей группы👨‍💻\n
Напиши мне: подписаться [Название_Группы] (без квадратной скобки)</strong>
        '''


def message_subscribe(username, username_group, sub_or_unsub):
    if sub_or_unsub:
        return f'<strong>Вы <em>{username}</em> успешно подписались на рассылку группы <em>{username_group}' \
               f'</em></strong>'
    else:
        return f'<strong>Вы <em>{username}</em> успешно отписались от рассылки на группу <em>{username_group}' \
               f'</em></strong>'


def message_theme(name, theme):
    return f'<strong>Вы <em>{name}</em> успешно выбрали рассылку темы: <em>{theme}</em></strong>'


"""
Here I will take the text and import into other .py files 

Тут будет текстовая информация, опять же эти файлы большие и занимают много место а к логике никак не относятся
"""
