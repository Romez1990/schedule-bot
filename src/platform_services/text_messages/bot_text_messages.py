class BotTextMessages:
    def message_text_start(self) -> str:
        return '''
        Приветствую дорогой студент👋или уже не студент\n
        🦾Я бот позволяющее предоставить тебе расписание твоей группы👨‍💻\n
        Напиши мне: /подписаться [Название_Группы] (без квадратной скобки)
                            '''

    def message_text_help(self) -> str:
        return '''
       /start - команда для старта бота (по умолчанию включен)\n
       /подписаться [Название_Группы] - подписаться на рассылку расписание\n
       /отписаться [Название_Группы] - отписаться от рассылки расписание\n
       /тема [тёмная/светлая] - получаться рассылку расписание в тёмной или светлой теме\n
                   '''

    def message_subscribe(self, username_group: str) -> str:
        return self.__messages_subscribe(username_group, True)

    def message_unsubscribe(self, username_group: str) -> str:
        return self.__messages_subscribe(username_group, False)

    def __messages_subscribe(self, username_group: str, sub_or_unsub: bool) -> str:
        subscribe = 'подписаться' if sub_or_unsub else 'отписаться'
        return f'Вы успешно {subscribe} на рассылку группы {username_group}'

    def message_theme(self, theme: str) -> str:
        return f'Вы успешно выбрали рассылку темы: {theme}'
