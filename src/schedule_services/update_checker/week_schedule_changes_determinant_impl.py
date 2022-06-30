from typing import (
    Sequence,
    Awaitable,
)

from infrastructure.ioc_container import service
from schedule_services.schedule import (
    Schedule,
    Group,
)
from .week_schedule_changes_determinant import WeekScheduleChangesDeterminant


@service
class WeekScheduleChangesDeterminantImpl(WeekScheduleChangesDeterminant):
    async def init(self) -> None:
        await self.__schedule_hash_storage.init()

    def get_changed_groups(self,
                           schedules: Sequence[Schedule]) -> Awaitable[Sequence[tuple[Schedule, Sequence[Group]]]]:
        ...
