from typing import (
    Sequence,
)

from infrastructure.ioc_container import service
from schedule_services.scraper import ScheduleScraper
from schedule_services.schedule import (
    Schedule,
)
from .schedule_update_fetcher import ScheduleUpdateFetcher
from .schedule_changes_determinant import ScheduleChangesDeterminant
from .group_schedule_changes_determinant import GroupScheduleChangesDeterminant


@service
class ScheduleUpdateFetcherImpl(ScheduleUpdateFetcher):
    def __init__(self, schedule_scraper: ScheduleScraper, schedule_changes_determinant: ScheduleChangesDeterminant,
                 group_schedule_changes_determinant: GroupScheduleChangesDeterminant) -> None:
        self.__schedule_scraper = schedule_scraper
        self.__schedule_changes_determinant = schedule_changes_determinant
        self.__group_schedule_changes_determinant = group_schedule_changes_determinant

    async def init(self) -> None:
        await self.__schedule_changes_determinant.init()
        await self.__group_schedule_changes_determinant.init()

    async def fetch_updates(self) -> tuple[Sequence[Schedule], Sequence[Schedule]]:
        schedules = await self.__schedule_scraper.scrap_schedules()
        changed_schedules = await self.__schedule_changes_determinant.get_changed_schedules(schedules)
        changes_schedules_and_groups = \
            await self.__group_schedule_changes_determinant.get_changed_groups(changed_schedules)
        return schedules, changes_schedules_and_groups
