from asyncio import (
    Event,
)
from typing import (
    NoReturn,
    Sequence,
    MutableSequence,
    Callable,
)

from infrastructure.ioc_container import service
from schedule_services.scraper import ScheduleScraper
from schedule_services.schedule import (
    Schedule,
    Group,
)
from .update_checker import UpdateChecker
from .fetcher_interval import FetchInterval
from .schedule_changes_determinant import ScheduleChangesDeterminant
from .week_schedule_changes_determinant import WeekScheduleChangesDeterminant


@service
class UpdateCheckerImpl(UpdateChecker):
    def __init__(self, schedule_scraper: ScheduleScraper, fetch_interval: FetchInterval,
                 schedule_changes_determinant: ScheduleChangesDeterminant,
                 week_schedule_changes_determinant: WeekScheduleChangesDeterminant) -> None:
        self.__schedule_scraper = schedule_scraper
        self.__fetch_interval = fetch_interval
        self.__schedule_changes_determinant = schedule_changes_determinant
        self.__week_schedule_changes_determinant = week_schedule_changes_determinant
        self.__schedules: Sequence[Schedule] | None = None
        self.__schedules_fetched = Event()
        self.__on_update: MutableSequence[Callable[[Schedule, Sequence[Group]], None]] = []

    def subscribe_to_updates(self, on_update: Callable[[Schedule, Sequence[Group]], None]) -> None:
        self.__on_update.append(on_update)

    async def start_checking_for_updates(self) -> NoReturn:
        while True:
            await self.__fetch_and_determine_changes()
            await self.__fetch_interval.wait()

    async def __fetch_and_determine_changes(self):
        self.__schedules = await self.__schedule_scraper.scrap_schedules()
        self.__schedules_fetched.set()
        changed_schedules = await self.__schedule_changes_determinant.get_changed_schedules(self.__schedules)
        a = await self.__week_schedule_changes_determinant.get_changed_groups(changed_schedules)

    def __on_schedules_changed(self, schedule: Schedule, groups: Sequence[Group]) -> None:
        for on_update in self.__on_update:
            on_update(schedule, groups)

    async def get_schedules(self) -> Sequence[Schedule]:
        await self.__schedules_fetched.wait()
        if self.__schedules is None:
            raise RuntimeError
        return self.__schedules
