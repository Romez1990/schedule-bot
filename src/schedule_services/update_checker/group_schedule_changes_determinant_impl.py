from typing import (
    Sequence,
    Awaitable,
)

from infrastructure.ioc_container import service
from schedule_services.schedule import (
    Schedule,
)
from .group_schedule_changes_determinant import GroupScheduleChangesDeterminant


@service
class GroupScheduleChangesDeterminantImpl(GroupScheduleChangesDeterminant):
    async def init(self) -> None:
        await self.__group_schedule_hash_storage.init()

    def get_changed_groups(self, schedules: Sequence[Schedule]) -> Awaitable[Sequence[Schedule]]:
        ...
