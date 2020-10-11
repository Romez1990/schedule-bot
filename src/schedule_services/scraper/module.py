from src.ioc_container import Module, Container
from .university_schedule import UniversityScheduleScraperModule
from .schedule_scraper_interface import ScheduleScraperInterface
from .schedule_scraper import ScheduleScraper


class ScraperModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(UniversityScheduleScraperModule)
        container.bind(ScheduleScraper).to(ScheduleScraperInterface)
