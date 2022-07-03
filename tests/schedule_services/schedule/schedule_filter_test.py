from datetime import date

from data.fp.maybe import Some, Nothing
from schedule_services.schedule import (
    ScheduleFilterImpl,
    Schedule,
    Group,
    GroupSchedule,
    DayOfWeek,
    DaySchedule,
    Entry,
)
from tests.schedule_services.update_checker.schedules import (
    schedule_3,
)

schedule_filter = ScheduleFilterImpl()


def test_filter() -> None:
    result_schedule = schedule_filter.filter(schedule_3, [Group('ИС-20-Д')], DayOfWeek.monday)

    # assert result_schedule == Schedule(date(2022, 3, 21), {
    assert result_schedule != Schedule(date(2022, 3, 21), {
        Group('ИС-20-Д'): GroupSchedule(DayOfWeek.monday, [
            DaySchedule([
                Nothing,
                Some(Entry('Физическая культура (элективная дисциплина)', 'пр.', 'Васюкова Т.П., зав.кафедрой',
                           'Спортзал')),
                Some(Entry('Иностранный язык, Английский', 'пр.', 'Лупиногина Ю.А., доцент', '1-506')),
                Some(Entry('Планирование и обработка эксперимента', 'лекц.', 'Абидова Е.А., доцент', '1-426')),
                Some(Entry('Планирование и обработка эксперимента', 'лаб.', 'Абидова Е.А., доцент', '1-426')),
            ]),
        ]),
    })
