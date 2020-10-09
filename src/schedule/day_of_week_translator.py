from .day_of_week_translator_interface import DayOfWeekTranslatorInterface
from .day_of_week import DayOfWeek


class DayOfWeekTranslator(DayOfWeekTranslatorInterface):
    __days_of_week = [
        'Понедельник',
        'Вторник',
        'Среда',
        'Четверг',
        'Пятница',
        'Суббота',
        'Воскресенье',
    ]

    def translate(self, day_of_week: DayOfWeek) -> str:
        return self.__days_of_week[day_of_week.value]
