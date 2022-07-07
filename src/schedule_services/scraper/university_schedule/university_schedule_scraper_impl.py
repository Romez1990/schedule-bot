from typing import (
    Sequence,
)

from infrastructure.ioc_container import service
from data.fp.task import Task
from data.vector import List
from schedule_services.schedule import (
    Schedule,
    ScheduleLinks,
    GroupSchedule,
)
from .university_schedule_scraper import UniversityScheduleScraper
from .schedule_links_scraper import ScheduleLinksScraper
from .group_schedule_scraper import GroupScheduleScraper


@service
class UniversityScheduleScraperImpl(UniversityScheduleScraper):
    def __init__(self, schedule_links_scraper: ScheduleLinksScraper,
                 group_schedule_scraper: GroupScheduleScraper) -> None:
        self.__schedule_links_scraper = schedule_links_scraper
        self.__group_schedule_scraper = group_schedule_scraper

    def scrap_schedules(self) -> Task[Sequence[Schedule]]:
        return self.__schedule_links_scraper.scrap_schedules_links() \
            .get_or_raise() \
            .bind(self.__get_schedules_from_links)

    def __get_schedules_from_links(self, links: Sequence[ScheduleLinks]) -> Task[Sequence[Schedule]]:
        tasks = List(links).map(self.__get_schedule_from_links_or_raise)
        return Task.parallel(*tasks)

    def __get_schedule_from_links_or_raise(self, links: ScheduleLinks) -> Task[Schedule]:
        return Task(self.__get_schedule_from_links(links))

    async def __get_schedule_from_links(self, links: ScheduleLinks) -> Schedule:
        starts_at = links.starts_at
        links = {group: schedule for group, schedule in links.items() if str(group) in ['ИС-20-Д', 'ИС-19-Д']}
        group_schedules_tasks = List(links.values()) \
            .map(self.__get_group_schedule)
        group_schedules = await Task.parallel(*group_schedules_tasks)
        schedule_dict = {group: group_schedule for group, group_schedule in zip(links.keys(), group_schedules)}
        return Schedule(starts_at, schedule_dict)

    def __get_group_schedule(self, link: str) -> Task[GroupSchedule]:
        return self.__group_schedule_scraper.scrap_group_schedule(link).get_or_raise()
