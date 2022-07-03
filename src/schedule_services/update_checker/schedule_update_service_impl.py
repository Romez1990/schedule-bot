from typing import (
    NoReturn,
    Sequence,
    MutableSequence,
    Callable,
)

from infrastructure.ioc_container import service
from schedule_services.schedule import (
    Schedule,
)
from .schedule_update_service import ScheduleUpdateService
from .schedule_update_fetcher import ScheduleUpdateFetcher
from .fetcher_interval import FetchInterval


@service
class ScheduleUpdateServiceImpl(ScheduleUpdateService):
    def __init__(self, schedule_update_fetcher: ScheduleUpdateFetcher, fetch_interval: FetchInterval) -> None:
        self.__schedule_update_fetcher = schedule_update_fetcher
        self.__fetch_interval = fetch_interval
        self.__schedules: Sequence[Schedule] | None = None
        self.__on_update: MutableSequence[Callable[[Sequence[Schedule]], None]] = []

    def subscribe_to_updates(self, on_update: Callable[[Sequence[Schedule]], None]) -> None:
        self.__on_update.append(on_update)

    async def init(self) -> None:
        await self.__schedule_update_fetcher.init()
        await self.__fetch_and_determine_changes()

    async def start_checking_for_updates(self) -> NoReturn:
        while True:
            await self.__fetch_interval.wait()
            await self.__fetch_and_determine_changes()

    async def __fetch_and_determine_changes(self) -> None:
        self.__schedules, changes_schedules_and_groups = await self.__schedule_update_fetcher.fetch_updates()
        if len(changes_schedules_and_groups) != 0:
            self.__on_schedules_changed(changes_schedules_and_groups)

    def __on_schedules_changed(self, changes_schedules_and_groups: Sequence[Schedule]) -> None:
        for on_update in self.__on_update:
            on_update(changes_schedules_and_groups)

    def get_schedules(self) -> Sequence[Schedule]:
        if self.__schedules is None:
            raise RuntimeError
        return self.__schedules
