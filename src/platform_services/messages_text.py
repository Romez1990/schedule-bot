class MessageText:
    def message_text_start(self) -> str:
        return '''
    <strong>Приветствую дорогой студент👋<strike>или уже не студент</strike>\n
    🦾Я бот позволяющее предоставить тебе расписание твоей группы👨‍💻\n
    Напиши мне: /подписаться [Название_Группы] (без квадратной скобки)</strong>
            '''

    def message_text_help(self) -> str:
        return '''
    <em>/start</em> - <strong>команда для старта бота</strong> (по умолчанию включен)\n
    <em>/подписаться [Название_Группы]</em> - <strong>подписаться на рассылку расписание</strong>\n
    <em>/отписаться [Название_Группы]</em> - <strong>отписаться от рассылки расписание</strong>\n
    <em>/тема [тёмная/светлая]</em> - <strong>получаться рассылку расписание в тёмной или светлой теме</strong>\n
            '''

    def message_subscribe(self, username_group: str) -> str:
        return self.__messages_subscribe(username_group, True)

    def message_unsubscribe(self, username_group: str) -> str:
        return self.__messages_subscribe(username_group, False)

    def __messages_subscribe(self, username_group: str, sub_or_unsub: bool) -> str:
        subscribe = 'подписаться' if sub_or_unsub else 'отписаться'
        return f'<strong>Вы успешно {subscribe} на рассылку группы <em>{username_group}' \
               f'</em></strong>'

    def message_theme(self, theme: str) -> str:
        return f'<strong>Вы успешно выбрали рассылку темы: <em>{theme}</em></strong>'
