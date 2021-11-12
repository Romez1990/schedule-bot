from .primitives import (
    TextComponent,
    Message,
    Paragraph,
    TextSpan,
    FontType,
)
from .messages_interface import MessagesInterface


class Messages(MessagesInterface):
    start = Message([
        Paragraph([
            TextSpan('Приветствую дорогой студент👋или уже не студент'),
        ]),
        Paragraph([
            TextSpan('Я бот позволяющее предоставить тебе расписание твоей группы👨‍💻'),
        ]),
        Paragraph([
            TextSpan('Напиши мне: /подписаться [Название_Группы] (без квадратной скобки)'),
        ]),
    ])

    help = Message([
        Paragraph([
            TextSpan('/start - команда для старта бота (по умолчанию включен)'),
        ]),
        Paragraph([
            TextSpan('/подписаться [Название_Группы] - подписаться на рассылку расписание'),
        ]),
        Paragraph([
            TextSpan('/отписаться [Название_Группы] - отписаться от рассылки расписание'),
        ]),
        Paragraph([
            TextSpan('/тема [тёмная/светлая] - получаться рассылку расписание в тёмной или светлой теме'),
        ]),
    ])

    def subscribe(self, group_name: str) -> TextComponent:
        return self.__messages_subscribe(group_name, True)

    def unsubscribe(self, group_name: str) -> TextComponent:
        return self.__messages_subscribe(group_name, False)

    def __messages_subscribe(self, group_name: str, subscribe_on_unsubscribe: bool) -> TextComponent:
        verb = 'подписаться' if subscribe_on_unsubscribe else 'отписаться'
        return TextSpan(f'Вы успешно {verb} на рассылку группы {group_name}')

    def change_theme(self, theme_name: str) -> TextComponent:
        return TextSpan(f'Вы успешно выбрали рассылку темы: {theme_name}')
