from .abstract_week_day_translator import AbstractWeekDayTranslator
from .week_day import WeekDay


class WeekDayTranslator(AbstractWeekDayTranslator):
    __week_days = [
        'Понедельник',
        'Вторник',
        'Среда',
        'Четверг',
        'Пятница',
        'Суббота',
        'Воскресенье',
    ]

    def translate(self, week_day: WeekDay) -> str:
        return self.__week_days[week_day.value]
