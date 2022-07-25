from typing import (
    Sequence,
)

from infrastructure.ioc_container import service
from data.fp.task import Task, taskify
from storage.entities import GroupScheduleHash
from .group_schedule_hash_repository import GroupScheduleHashRepository


@service
class GroupScheduleHashRepositoryImpl(GroupScheduleHashRepository):
    @taskify
    async def find_all(self) -> Sequence[GroupScheduleHash]: ...

    def save_all(self, schedule_hashes: Sequence[GroupScheduleHash]) -> Task[Sequence[GroupScheduleHash]]: ...

    def update_all(self, schedule_hashes: Sequence[GroupScheduleHash]) -> Task[None]: ...

    def delete_all(self, schedule_hashes: Sequence[GroupScheduleHash]) -> Task[None]: ...
