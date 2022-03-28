from asyncio import (
    Event,
)
from typing import (
    NoReturn,
    Sequence,
    Callable,
)

from infrastructure.ioc_container import service
from schedule_services.schedule import (
    Schedule,
    Group,
)
from .schedule_update_service import ScheduleUpdateService
from .schedule_fetcher import ScheduleFetcher
from .update_checker_factory import UpdateCheckerFactory


@service
class ScheduleUpdateServiceImpl(ScheduleUpdateService):
    def __init__(self, schedule_fetcher: ScheduleFetcher, update_checker_factory: UpdateCheckerFactory) -> None:
        schedule_fetcher.subscribe_for_updates(self.__on_schedules_fetched)
        self.__schedule_fetcher = schedule_fetcher
        self.__update_checker = update_checker_factory.create(self.__on_schedules_changed)
        self.__schedules: Sequence[Schedule] | None = None
        self.__schedules_fetched = Event()
        self.__on_update: list[Callable[[Schedule, Sequence[Group]], None]] = []

    def __on_schedules_fetched(self, schedules: Sequence[Schedule]) -> None:
        self.__schedules = schedules
        self.__schedules_fetched.set()

    def __on_schedules_changed(self, schedule: Schedule, groups: Sequence[Group]) -> None:
        for on_update in self.__on_update:
            on_update(schedule, groups)

    def subscribe_for_updates(self, on_update: Callable[[Schedule, Sequence[Group]], None]) -> None:
        self.__on_update.append(on_update)

    async def start_checking_updates(self) -> NoReturn:
        await self.__schedule_fetcher.start()

    async def get_schedules(self) -> Sequence[Schedule]:
        await self.__schedules_fetched.wait()
        if self.__schedules is None:
            raise RuntimeError
        return self.__schedules
