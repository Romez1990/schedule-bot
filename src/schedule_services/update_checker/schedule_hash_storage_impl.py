from datetime import date
from typing import (
    Sequence,
    MutableMapping,
)

from infrastructure.ioc_container import service
from infrastructure.config import Config
from data.fp.maybe import Maybe, Some, Nothing
from data.fp.task import Task, taskify
from data.vector import List
from storage.repositories import ScheduleHashRepository
from storage.entities import ScheduleHash
from .schedule_hash_storage import ScheduleHashStorage


@service
class ScheduleHashStorageImpl(ScheduleHashStorage):
    def __init__(self, schedule_hash_repository: ScheduleHashRepository, config: Config) -> None:
        self.__schedule_hash_repository = schedule_hash_repository
        self.__config = config
        self.__hashes: MutableMapping[date, ScheduleHash] = {}

    @property
    def __max_size(self) -> int:
        return self.__config.weeks_to_store_schedule_hash

    @taskify
    async def init(self) -> None:
        hashes = await self.__schedule_hash_repository.get_all()
        self.__hashes = {schedule_hash.starts_at: schedule_hash for schedule_hash in hashes}

    def get_hashes_by_dates(self, schedule_dates: Sequence[date]) -> Sequence[Maybe[int]]:
        return List(schedule_dates).map(self.__get_hash_from_schedule_hash)

    def __get_hash_from_schedule_hash(self, schedule_date: date) -> Maybe[int]:
        return Maybe.from_optional(self.__hashes.get(schedule_date)) \
            .map(self.__get_int_hash)

    def __get_int_hash(self, schedule_hash: ScheduleHash) -> int:
        return schedule_hash.hash

    @taskify
    async def save(self, hashes: Sequence[tuple[date, int]]) -> None:
        results = List(hashes).map(self.__process_hash)
        hashes_to_save, hashes_to_update, hashes_to_delete = List(zip(*results)) \
            .map(List.flatten) \
            .map(self.__hashes_to_maybe)
        new_hashes, *_ = await Task.parallel(
            hashes_to_save.map(self.__schedule_hash_repository.save_all).get_or_call(lambda: Task.from_value([])),
            hashes_to_update.map(self.__schedule_hash_repository.update_all).get_or_call(lambda: Task.from_value(None)),
            hashes_to_delete.map(self.__schedule_hash_repository.delete_all).get_or_call(lambda: Task.from_value(None)),
        )
        self.__hashes.update({new_hash.starts_at: new_hash for new_hash in new_hashes})

    def __process_hash(self, hash_tuple: tuple[date, int]
                       ) -> tuple[Sequence[ScheduleHash], Sequence[ScheduleHash], Sequence[ScheduleHash]]:
        date_of_hash, int_hash = hash_tuple
        hashes_to_save = []
        hashes_to_update = []
        hashes_to_delete = []
        schedule_hash = self.__hashes.get(date_of_hash)
        if schedule_hash is None:
            while len(self.__hashes) >= self.__max_size:
                hashes_to_delete.append(self.__delete_hash())
            hashes_to_save.append(self.__create_hash(date_of_hash, int_hash))
        else:
            hashes_to_update.append(self.__update_hash(schedule_hash, int_hash))
        return hashes_to_save, hashes_to_update, hashes_to_delete

    def __delete_hash(self) -> ScheduleHash:
        oldest_date = min(self.__hashes)
        return self.__hashes.pop(oldest_date)

    def __create_hash(self, date_of_hash: date, int_hash: int) -> ScheduleHash:
        schedule_hash = ScheduleHash(date_of_hash, int_hash)
        self.__hashes[schedule_hash.starts_at] = schedule_hash
        return schedule_hash

    def __update_hash(self, schedule_hash: ScheduleHash, int_hash: int) -> ScheduleHash:
        new_schedule_hash = schedule_hash.set_hash(int_hash)
        self.__hashes[new_schedule_hash.starts_at] = new_schedule_hash
        return new_schedule_hash

    def __hashes_to_maybe(self, hashes: Sequence[ScheduleHash]) -> Maybe[Sequence[ScheduleHash]]:
        if len(hashes) == 0:
            return Nothing
        return Some(hashes)
