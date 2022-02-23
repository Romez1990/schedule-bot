from typing import (
    NoReturn,
    Callable,
    Sequence,
)

from infrastructure.ioc_container import service
from infrastructure.config import Config
from schedule_services.scraper import ScheduleScraper
from schedule_services.schedule import Schedule
from .schedule_fetcher_factory import ScheduleFetcherFactory
from .schedule_fetcher import ScheduleFetcher
from .schedule_fetcher_impl import ScheduleFetcherImpl


@service
class ScheduleFetcherFactoryImpl(ScheduleFetcherFactory):
    def __init__(self, schedule_scraper: ScheduleScraper, config: Config) -> None:
        self.__schedule_scraper = schedule_scraper
        self.__config = config

    def create(self, on_schedules_fetched: Callable[[Sequence[Schedule]], None]) -> ScheduleFetcher:
        return ScheduleFetcherImpl(self.__schedule_scraper, self.__config, on_schedules_fetched)
