from pytest import (
    mark,
)

from schedule_services.schedule import (
    DayOfWeekTranslatorImpl,
    DayOfWeek,
)

day_of_week_translator = DayOfWeekTranslatorImpl()


@mark.parametrize('day_of_week,translated', [
    (DayOfWeek.monday, 'Понедельник'),
    (DayOfWeek.tuesday, 'Вторник'),
    (DayOfWeek.wednesday, 'Среда'),
    (DayOfWeek.thursday, 'Четверг'),
    (DayOfWeek.friday, 'Пятница'),
    (DayOfWeek.saturday, 'Суббота'),
    (DayOfWeek.sunday, 'Воскресенье'),
])
def test_init__calls_init_of_determinants(day_of_week: DayOfWeek, translated: str) -> None:
    result = day_of_week_translator.translate(day_of_week)

    assert result == translated
