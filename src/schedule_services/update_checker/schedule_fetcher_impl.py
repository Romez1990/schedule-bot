from asyncio import sleep
from typing import (
    NoReturn,
    Callable,
    Sequence,
)

from infrastructure.ioc_container import service
from infrastructure.config import Config
from schedule_services.scraper import ScheduleScraper
from schedule_services.schedule import Schedule
from .schedule_fetcher import ScheduleFetcher


@service
class ScheduleFetcherImpl(ScheduleFetcher):
    def __init__(self, schedule_scraper: ScheduleScraper, config: Config,
                 on_schedules_fetched: Callable[[Sequence[Schedule]], None]) -> None:
        self.__schedule_scraper = schedule_scraper
        self.__interval = config.update_checker_interval
        self.__on_schedules_fetched = on_schedules_fetched

    async def start(self) -> NoReturn:
        while True:
            schedules = await self.__schedule_scraper.scrap_schedules()
            self.__on_schedules_fetched(schedules)
            await self.__wait()

    async def __wait(self) -> None:
        minutes = self.__interval
        seconds = minutes * 60
        await sleep(seconds)
