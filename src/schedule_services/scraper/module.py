from src.ioc_container import Module, ContainerBuilder
from .university_schedule import UniversityScheduleScraperModule
from .schedule_scraper_interface import ScheduleScraperInterface
from .schedule_scraper import ScheduleScraper


class ScraperModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.register_module(UniversityScheduleScraperModule)
        builder.bind(ScheduleScraperInterface).to(ScheduleScraper)
