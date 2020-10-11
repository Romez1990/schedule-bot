from src.schedule import (
    Schedule,
)
from .schedule_scraper_interface import ScheduleScraperInterface
from .university_schedule import UniversityScheduleScraperInterface


class ScheduleScraper(ScheduleScraperInterface):
    def __init__(self, university_schedule_scraper: UniversityScheduleScraperInterface) -> None:
        self.__university_schedule_scraper = university_schedule_scraper

    async def get_schedule(self) -> Schedule:
        university_schedule = await self.__university_schedule_scraper.get_schedule()
        return university_schedule
