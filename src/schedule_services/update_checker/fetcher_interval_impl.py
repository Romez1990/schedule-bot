from asyncio import sleep

from infrastructure.ioc_container import service
from infrastructure.config import Config
from .fetcher_interval import FetchInterval


@service
class FetchIntervalImpl(FetchInterval):
    def __init__(self, config: Config) -> None:
        self.__config = config

    @property
    def __interval(self) -> int:
        return self.__minutes_to_seconds(self.__config.update_checker_interval)

    def __minutes_to_seconds(self, minutes: int) -> int:
        return minutes * 60

    async def wait(self) -> None:
        await sleep(self.__interval)
