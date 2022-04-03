from datetime import date
from asyncio import sleep
from typing import (
    Callable,
    Sequence,
)
from pytest import (
    fixture,
    mark,
)
from unittest.mock import Mock

from data.fp.maybe import Some, Nothing
from data.fp.task import Task
from data.serializers import BytesSerializerImpl
from schedule_services.schedule import (
    Schedule,
    Group,
    WeekSchedule,
    DayOfWeek,
    DaySchedule,
    Entry,
)
from schedule_services.update_checker import (
    UpdateCheckerImpl,
    ScheduleFetcher,
    ScheduleHashing,
    ScheduleHashStorage,
)


@fixture(autouse=True)
def setup() -> None:
    global update_checker, schedule_fetcher, schedule_hashing, schedule_hash_storage, on_schedules_changed
    schedule_fetcher = Mock()

    def create_schedule_fetcher(on_schedules_fetched: Callable[[Sequence[Schedule]], None]) -> None:
        global schedules_fetched
        schedules_fetched = on_schedules_fetched

    schedule_fetcher.subscribe_for_updates = create_schedule_fetcher
    schedule_hashing = Mock()
    schedule_hash_storage = Mock()
    on_schedules_changed = Mock()
    update_checker = UpdateCheckerImpl(schedule_fetcher, schedule_hashing, schedule_hash_storage, on_schedules_changed)


update_checker: UpdateCheckerImpl
schedules_fetched: Callable[[Sequence[Schedule]], None]
schedule_fetcher: ScheduleFetcher
schedule_hashing: ScheduleHashing
schedule_hash_storage: ScheduleHashStorage
on_schedules_changed: Callable[[Schedule, list[Group]], None]


@mark.asyncio
async def test_schedule_fetched__saves_hash_to_storage__when_no_hash_found_in_storage() -> None:
    schedule_hash = 123
    schedule_hashing.hash = Mock(return_value=schedule_hash)
    schedule_hash_storage.get_hashes_by_dates = Mock(return_value=Task.from_value([Nothing]))
    schedule_hash_storage.save = Mock()

    schedules_fetched([schedule])

    await sleep(0)
    schedule_hashing.hash.assert_called_once_with(schedule)
    schedule_hash_storage.get_hashes_by_dates.assert_called_once_with([schedule.starts_at])
    schedule_hash_storage.save.assert_called_once_with([(schedule.starts_at, schedule_hash)])


schedule = Schedule(date(2022, 3, 21), {
    Group('ИС-20-Д'): WeekSchedule(DayOfWeek.monday, [
        DaySchedule([
            Nothing,
            Some(
                Entry('Физическая культура (элективная дисциплина)', 'пр.', 'Васюкова Т.П., зав.кафедрой', 'Спортзал')),
            Some(Entry('Иностранный язык, Английский', 'пр.', 'Лупиногина Ю.А., доцент', '1-506')),
            Some(Entry('Планирование и обработка эксперимента', 'лекц.', 'Абидова Е.А., доцент', '1-426')),
        ]),
        DaySchedule([
            Some(Entry('Общая энергетика', 'лекц.', 'Смолин А.Ю., доцент', '1-308')),
            Some(
                Entry('Физическая культура (элективная дисциплина)', 'пр.', 'Васюкова Т.П., зав.кафедрой', 'Спортзал')),
            Some(Entry('Теория вероятностей. Математическая статистика', 'лекц.', 'Чабанова Н.И., ст. преподаватель',
                       '1-518')),
        ]),
        DaySchedule([
            Nothing,
            Some(Entry('Мультимедиа технологии', 'лекц.', 'Хегай Л.С., доцент', '3-102')),
            Some(Entry('Мультимедиа технологии,', 'лаб.', 'Хегай Л.С., доцент', '3-102')),
            Some(Entry('Мультимедиа технологии,', 'лаб.', 'Хегай Л.С., доцент', '3-102')),
        ]),
        DaySchedule([
            Some(Entry('Основы математического моделирования и численные м', 'лекц.', 'Козоброд В.Н., доцент', 'ДО')),
            Nothing,
            Some(Entry('Архитектура ЭВМ', 'лекц.', 'Кривин В.В., профессор', '1-405')),
            Some(Entry('Теория вероятностей. Математическая статистика', 'пр.', 'Чабанова Н.И., ст. преподаватель',
                       '1-519')),
        ]),
        DaySchedule([
            Some(Entry('Инфокоммуникационные системы и сети', 'лекц.', 'Цвелик Е.А., доцент', '1-415')),
            Some(Entry('Иностранный язык, Английский', 'пр.', 'Лупиногина Ю.А., доцент', '1-506')),
        ]),
    ]),
})

schedule_3 = Schedule(date(2022, 3, 21), {
    Group('ИС-20-Д'): WeekSchedule(DayOfWeek.monday, [
        DaySchedule([
            Nothing,
            Some(
                Entry('Физическая культура (элективная дисциплина)', 'пр.', 'Васюкова Т.П., зав.кафедрой', 'Спортзал')),
            Some(Entry('Иностранный язык, Английский', 'пр.', 'Лупиногина Ю.А., доцент', '1-506')),
            Some(Entry('Планирование и обработка эксперимента', 'лекц.', 'Абидова Е.А., доцент', '1-426')),
            Some(Entry('Планирование и обработка эксперимента', 'лаб.', 'Абидова Е.А., доцент', '1-426')),
        ]),
        DaySchedule([
            Some(Entry('Общая энергетика', 'лекц.', 'Смолин А.Ю., доцент', '1-308')),
            Some(
                Entry('Физическая культура (элективная дисциплина)', 'пр.', 'Васюкова Т.П., зав.кафедрой', 'Спортзал')),
            Some(Entry('Теория вероятностей. Математическая статистика', 'лекц.', 'Чабанова Н.И., ст. преподаватель',
                       '1-518')),
            Some(Entry('Инфокоммуникационные системы и сети', 'лаб.', 'Толстов В.А., доцент', '1-418')),
        ]),
        DaySchedule([
            Nothing,
            Some(Entry('Мультимедиа технологии', 'лекц.', 'Хегай Л.С., доцент', '3-102')),
            Some(Entry('Мультимедиа технологии,', 'лаб.', 'Хегай Л.С., доцент', '3-102')),
            Some(Entry('Мультимедиа технологии,', 'лаб.', 'Хегай Л.С., доцент', '3-102')),
        ]),
        DaySchedule([
            Nothing,
            Nothing,
            Some(Entry('Основы математического моделирования и численные м', 'лекц.', 'Козоброд В.Н., доцент', 'ДО')),
            Nothing,
            Some(Entry('Архитектура ЭВМ', 'лекц.', 'Кривин В.В., профессор', '1-405')),
            Some(Entry('Теория вероятностей. Математическая статистика', 'пр.', 'Чабанова Н.И., ст. преподаватель',
                       '1-519')),
        ]),
        DaySchedule([
            Nothing,
            Nothing,
            Some(Entry('Инфокоммуникационные системы и сети', 'лекц.', 'Цвелик Е.А., доцент', '1-415')),
            Some(Entry('Иностранный язык, Английский', 'пр.', 'Лупиногина Ю.А., доцент', '1-506')),
        ]),
        DaySchedule([
            Some(Entry('Операционные системы', 'лекц.', 'Стороженко А.С., ст. преподаватель', '1-415')),
            Some(Entry('Операционные системы', 'лаб.', 'Стороженко А.С., ст. преподаватель', '1-426')),
            Some(Entry('Архитектура ЭВМ', 'лаб.', 'Толстов В.А., доцент', '1-418')),
        ]),
    ]),
    Group('ИС-19-Д'): WeekSchedule(DayOfWeek.monday, [
        DaySchedule([
            Some(Entry('Теория информационных процессов и систем', 'лекц.', 'Чернов А.В., профессор', '1-410')),
            Some(Entry('Web-программирование', 'лекц.', 'Хегай Л.С., доцент', '1-410')),
        ]),
        DaySchedule([
            Nothing,
            Nothing,
            Some(Entry('Управление данными', 'лекц.', 'Цвелик Е.А., доцент', '1-410')),
            Some(Entry('Управление данными', 'лаб.', 'Цвелик Е.А., доцент', '1-410')),
            Some(Entry('Физическая культура (элективная дисциплина)', 'пр.', 'Коваленко С.П., ст. преподаватель',
                       'Спортзал')),
        ]),
        DaySchedule([
            Nothing,
            Some(Entry('Культура безопасности', 'лекц.', 'Руденко В.А., профессор', 'актовый зал')),
            Some(Entry('Экономика', 'лекц.', 'Ефименко Н.А., доцент', '1-518')),
        ]),
        DaySchedule([
            Nothing,
            Some(Entry('Методы оптимальных решений', 'лекц.', 'Цуверкалова О.Ф., и.о. зав.кафедрой', '1-412')),
            Some(Entry('Администрирование в информационных системах', 'лекц.', 'Толстов В.А., доцент', '1-418')),
            Some(Entry('Администрирование в информационных системах', 'лаб.', 'Толстов В.А., доцент', '1-418')),
        ]),
        DaySchedule([]),
        DaySchedule([
            Some(Entry('Информационные технологии', 'лекц.', 'Толстов В.А., доцент', '1-405')),
            Some(Entry('Информационные технологии', 'лаб.', 'Толстов В.А., доцент', '1-405')),
        ]),
    ]),
})


def change_schedule() -> Schedule:
    serializer = BytesSerializerImpl()
    schedule_bytes = serializer.serialize(schedule)
    schedule_2 = serializer.deserialize(schedule_bytes, Schedule)
    group_schedule = schedule_2._data[Group('ИС-20-Д')]
    friday_schedule = group_schedule._WeekSchedule__day_schedules[-1]
    friday_entries = list(friday_schedule._DaySchedule__entries)
    friday_entries[0] = Nothing
    friday_schedule._DaySchedule__entries = tuple(friday_entries)
    return schedule_2


schedule_2 = change_schedule()
