from src.ioc_container import Module, ContainerBuilder
from .university_schedule_scraper_interface import UniversityScheduleScraperInterface
from .university_schedule_scraper import UniversityScheduleScraper
from .group_list_scraper_interface import GroupListScraperInterface
from .group_list_scraper import GroupListScraper
from .group_schedule_scraper_interface import GroupScheduleScraperInterface
from .group_schedule_scraper import GroupScheduleScraper
from .schedule_post_processor_interface import SchedulePostProcessorInterface
from .schedule_post_processor import SchedulePostProcessor


class UniversityScheduleScraperModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(UniversityScheduleScraperInterface).to(UniversityScheduleScraper)
        builder.bind(GroupListScraperInterface).to(GroupListScraper)
        builder.bind(GroupScheduleScraperInterface).to(GroupScheduleScraper)
        builder.bind(SchedulePostProcessorInterface).to(SchedulePostProcessor)