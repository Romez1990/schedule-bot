from typing import (
    Sequence,
)

from infrastructure.ioc_container import service
from data.fp.task import Task
from data.vector import List
from schedule_services.schedule import (
    Schedule,
    ScheduleLinks,
    WeekSchedule,
)
from .university_schedule_scraper import UniversityScheduleScraper
from .schedule_links_scraper import ScheduleLinksScraper
from .week_schedule_scraper import WeekScheduleScraper
from .schedule_post_processor import SchedulePostProcessor


@service
class UniversityScheduleScraperImpl(UniversityScheduleScraper):
    def __init__(self, schedule_links_scraper: ScheduleLinksScraper, group_schedule_scraper: WeekScheduleScraper,
                 schedule_post_processor: SchedulePostProcessor) -> None:
        self.__schedule_links_scraper = schedule_links_scraper
        self.__group_schedule_scraper = group_schedule_scraper
        self.__schedule_post_processor = schedule_post_processor

    def scrap_schedule(self) -> Task[Sequence[Schedule]]:
        return self.__schedule_links_scraper.scrap_schedule_links() \
            .get_or_raise() \
            .bind(self.__get_schedules_from_links)

    def __get_schedules_from_links(self, links: Sequence[ScheduleLinks]) -> Task[Sequence[Schedule]]:
        tasks = List(links).map(self.__get_schedule_from_links_or_raise)
        return Task.parallel(tasks)

    def __get_schedule_from_links_or_raise(self, links: ScheduleLinks) -> Task[Schedule]:
        return Task(self.__get_schedule_from_links(links))

    async def __get_schedule_from_links(self, links: ScheduleLinks) -> Schedule:
        week_start = links.week_start
        week_end = links.week_end
        links_dict = dict(links)
        week_schedules_tasks = List(links_dict.values()).map(self.__get_week_schedule)
        week_schedules = await Task.parallel(week_schedules_tasks)
        schedule_dict = {group: week_schedule for group, week_schedule in zip(links_dict.keys(), week_schedules)}
        schedule = Schedule(week_start, week_end, schedule_dict)
        return self.__schedule_post_processor.process(schedule)

    def __get_week_schedule(self, link: str) -> Task[WeekSchedule]:
        return self.__group_schedule_scraper.scrap_week_schedule(link).get_or_raise()
