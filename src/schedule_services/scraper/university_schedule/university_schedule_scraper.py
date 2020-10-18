from asyncio import gather
from typing import (
    List,
    Dict,
)

from src.schedule import (
    Schedule,
    Group,
    UniversityGroup,
    GroupSchedule,
)
from .university_schedule_scraper_interface import UniversityScheduleScraperInterface
from .group_list_scraper_interface import GroupListScraperInterface
from .group_schedule_scraper_interface import GroupScheduleScraperInterface
from .schedule_post_processor_interface import SchedulePostProcessorInterface


class UniversityScheduleScraper(UniversityScheduleScraperInterface):
    def __init__(self, group_list_scraper: GroupListScraperInterface,
                 group_schedule_scraper: GroupScheduleScraperInterface,
                 schedule_post_processor: SchedulePostProcessorInterface) -> None:
        self.__group_list_scraper = group_list_scraper
        self.__group_schedule_scraper = group_schedule_scraper
        self.__schedule_post_processor = schedule_post_processor

    async def get_schedule(self) -> Schedule:
        groups_and_links = await self.__group_list_scraper.get_groups_and_links()
        schedule_dict = await self.__get_group_schedules(groups_and_links)
        schedule = Schedule(schedule_dict)
        return self.__schedule_post_processor.process(schedule)

    async def __get_group_schedules(self, groups_and_links: Dict[UniversityGroup, str]) -> Dict[Group, GroupSchedule]:
        groups = [group for group in groups_and_links]
        group_schedule_coroutines = [self.__group_schedule_scraper.get_group_schedule(link)
                                     for group, link in groups_and_links.items()]
        group_schedules: List[GroupSchedule] = await gather(*group_schedule_coroutines)
        groups_and_group_schedules = zip(groups, group_schedules)
        return {group: group_schedule for group, group_schedule in groups_and_group_schedules}
