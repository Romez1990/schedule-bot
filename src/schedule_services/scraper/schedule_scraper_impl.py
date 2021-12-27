from typing import (
    Sequence,
)

from data.fp.task import Task
from infrastructure.ioc_container import service
from schedule_services.schedule import Schedule
from .schedule_scraper import ScheduleScraper
from .university_schedule import UniversityScheduleScraper


@service
class ScheduleScraperImpl(ScheduleScraper):
    def __init__(self, university_schedule_scraper: UniversityScheduleScraper) -> None:
        self.__university_schedule_scraper = university_schedule_scraper

    def scrap_schedule(self) -> Task[Sequence[Schedule]]:
        university_schedule = self.__university_schedule_scraper.scrap_schedule()
        return university_schedule
