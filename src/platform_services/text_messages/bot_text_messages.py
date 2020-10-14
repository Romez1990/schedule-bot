class BotTextMessages:
    def message_text_start(self, platform: str) -> str:
        return '''
                    Приветствую дорогой студент👋или уже не студент\n
                    🦾Я бот позволяющее предоставить тебе расписание твоей группы👨‍💻\n
                    Напиши мне: /подписаться [Название_Группы] (без квадратной скобки)
                            '''

    def message_text_help(self, platform: str) -> str:
        if platform == 'telegram':
            return '''
        <em>/start</em> - <strong>команда для старта бота</strong> (по умолчанию включен)\n
        <em>/подписаться [Название_Группы]</em> - <strong>подписаться на рассылку расписание</strong>\n
        <em>/отписаться [Название_Группы]</em> - <strong>отписаться от рассылки расписание</strong>\n
        <em>/тема [тёмная/светлая]</em> - <strong>получаться рассылку расписание в тёмной или светлой теме</strong>\n
                '''
        elif platform == 'vk':
            return '''
                   /start - <strong>команда для старта бота (по умолчанию включен)\n
                   /подписаться [Название_Группы] - подписаться на рассылку расписание\n
                   /отписаться [Название_Группы] - отписаться от рассылки расписание\n
                   /тема [тёмная/светлая] - получаться рассылку расписание в тёмной или светлой теме\n
                   '''
        else:
            return 'Error'

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
