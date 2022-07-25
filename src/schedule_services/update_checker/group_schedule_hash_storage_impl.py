from datetime import date
from typing import (
    Sequence,
    Mapping,
    MutableMapping,
)

from infrastructure.ioc_container import service
from infrastructure.config import Config
from data.fp.maybe import Maybe, Some, Nothing
from data.fp.task import Task, taskify
from data.vector import List
from schedule_services.schedule import Group
from storage.repositories import GroupScheduleHashRepository
from storage.entities import GroupScheduleHash
from .group_schedule_hash_storage import GroupScheduleHashStorage


@service
class GroupScheduleHashStorageImpl(GroupScheduleHashStorage):
    def __init__(self, group_schedule_hash_repository: GroupScheduleHashRepository, config: Config) -> None:
        self.__group_schedule_hash_repository = group_schedule_hash_repository
        self.__config = config
        self.__hashes: MutableMapping[date, MutableMapping[Group, GroupScheduleHash]] = {}

    @property
    def __max_size(self) -> int:
        return self.__config.weeks_to_store_schedule_hash

    @taskify
    async def init(self) -> None:
        group_schedule_hashes = await self.__group_schedule_hash_repository.find_all()
        List(group_schedule_hashes).map(...)

    # def __

    def get_hashes_by_dates(self, schedule_dates: Sequence[tuple[date, Sequence[Group]]]
                            ) -> Sequence[Mapping[Group, Maybe[int]]]: ...

    def save(self, hashes: Sequence[tuple[date, Sequence[tuple[Group, int]]]]) -> Task[None]: ...
