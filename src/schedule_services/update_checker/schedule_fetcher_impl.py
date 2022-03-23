from asyncio import sleep
from typing import (
    NoReturn,
    Callable,
    Sequence,
    Awaitable,
)

from infrastructure.ioc_container import service
from infrastructure.config import Config
from schedule_services.scraper import ScheduleScraper
from schedule_services.schedule import Schedule
from .schedule_fetcher import ScheduleFetcher


@service
class ScheduleFetcherImpl(ScheduleFetcher):
    def __init__(self, schedule_scraper: ScheduleScraper, config: Config) -> None:
        self.__schedule_scraper = schedule_scraper
        self.__interval = self.__minutes_to_seconds(config.update_checker_interval)
        self.__on_schedules_fetched: list[Callable[[Sequence[Schedule]], Awaitable[None]]] = []

    def __minutes_to_seconds(self, minutes: int) -> int:
        return minutes * 60

    async def start(self) -> NoReturn:
        while True:
            schedules = await self.__schedule_scraper.scrap_schedules()
            for on_schedules_fetched in self.__on_schedules_fetched:
                on_schedules_fetched(schedules)
            await sleep(self.__interval)

    def subscribe_for_updates(self, on_schedules_fetched: Callable[[Sequence[Schedule]], Awaitable[None]]) -> None:
        self.__on_schedules_fetched.append(on_schedules_fetched)