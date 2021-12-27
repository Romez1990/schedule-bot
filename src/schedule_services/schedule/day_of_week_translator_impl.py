from infrastructure.ioc_container import service
from .day_of_week_translator import DayOfWeekTranslator
from .day_of_week import DayOfWeek


@service
class DayOfWeekTranslatorImpl(DayOfWeekTranslator):
    __days_of_week = (
        'Понедельник',
        'Вторник',
        'Среда',
        'Четверг',
        'Пятница',
        'Суббота',
        'Воскресенье',
    )

    def translate(self, day_of_week: DayOfWeek) -> str:
        return self.__days_of_week[day_of_week.value]
