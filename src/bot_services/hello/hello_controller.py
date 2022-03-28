from datetime import date

from data.fp.maybe import Some, Nothing
from messenger_services.messenger_service import (
    MessengerController,
    MessengerAdapter,
    Message,
    controller,
    message_handler,
)
from schedule_services.schedule import (
    Schedule,
    WeekSchedule,
    DayOfWeek,
    DaySchedule,
    Entry,
)
from schedule_services.renderer import ScheduleRenderer
from schedule_services.schedule import Group, ScheduleFilter
from schedule_services.scraper import ScheduleScraper


@controller
class HelloController(MessengerController):
    def __init__(self, schedule_scraper: ScheduleScraper, schedule_filter: ScheduleFilter, renderer: ScheduleRenderer, adapter: MessengerAdapter) -> None:
        super().__init__(adapter)
        self.__schedule_scraper = schedule_scraper
        self.__schedule_filter = schedule_filter
        self.__renderer = renderer

    @message_handler('start')
    async def start(self, message: Message) -> None:
        schedule = Schedule(date(2022, 3, 21), {
            Group('ИС-20-Д'): WeekSchedule(DayOfWeek.monday, [
                DaySchedule([
                    Nothing,
                    Some(
                        Entry('Физическая культура (элективная дисциплина)', 'пр.', 'Васюкова Т.П., зав.кафедрой',
                              'Спортзал')),
                    Some(Entry('Иностранный язык, Английский', 'пр.', 'Лупиногина Ю.А., доцент', '1-506')),
                    Some(Entry('Планирование и обработка эксперимента', 'лекц.', 'Абидова Е.А., доцент', '1-426')),
                ]),
                DaySchedule([
                    Some(Entry('Общая энергетика', 'лекц.', 'Смолин А.Ю., доцент', '1-308')),
                    Some(
                        Entry('Физическая культура (элективная дисциплина)', 'пр.', 'Васюкова Т.П., зав.кафедрой',
                              'Спортзал')),
                    Some(Entry('Теория вероятностей. Математическая статистика', 'лекц.',
                               'Чабанова Н.И., ст. преподаватель',
                               '1-518')),
                ]),
                DaySchedule([
                    Nothing,
                    Some(Entry('Мультимедиа технологии', 'лекц.', 'Хегай Л.С., доцент', '3-102')),
                    Some(Entry('Мультимедиа технологии,', 'лаб.', 'Хегай Л.С., доцент', '3-102')),
                    Some(Entry('Мультимедиа технологии,', 'лаб.', 'Хегай Л.С., доцент', '3-102')),
                ]),
                DaySchedule([
                    Some(Entry('Основы математического моделирования и численные м', 'лекц.', 'Козоброд В.Н., доцент',
                               'ДО')),
                    Nothing,
                    Some(Entry('Архитектура ЭВМ', 'лекц.', 'Кривин В.В., профессор', '1-405')),
                    Some(Entry('Теория вероятностей. Математическая статистика', 'пр.',
                               'Чабанова Н.И., ст. преподаватель',
                               '1-519')),
                ]),
                DaySchedule([
                    Some(Entry('Инфокоммуникационные системы и сети', 'лекц.', 'Цвелик Е.А., доцент', '1-415')),
                    Some(Entry('Иностранный язык, Английский', 'пр.', 'Лупиногина Ю.А., доцент', '1-506')),
                ]),
            ]),
        })
        dark_schedule = self.__renderer.render(schedule, 'dark')
        await self._send_message(message.user, 'Появилось расписание на следующую неделю')
        await self._send_image(message.user, dark_schedule)

    @message_handler('help')
    async def help(self, message: Message) -> None:
        await self._send_message(message.user, 'Sorry, I have not been taught to help yet')
