from datetime import date
from typing import (
    Callable,
    Sequence,
    cast,
)

from infrastructure.ioc_container import service
from data.fp.function import const
from data.fp.maybe import Maybe, Some, Nothing
from data.fp.task import Task
from data.vector import List
from data.hashing import Md5ObjectHashing
from schedule_services.schedule import Schedule
from .schedule_changes_determinant import ScheduleChangesDeterminant
from .schedule_hash_storage import ScheduleHashStorage


@service
class ScheduleChangesDeterminantImpl(ScheduleChangesDeterminant):
    def __init__(self, object_hashing: Md5ObjectHashing, schedule_hash_storage: ScheduleHashStorage) -> None:
        self.__object_hashing = object_hashing
        self.__schedule_hash_storage = schedule_hash_storage

    async def get_changed_schedules(self, schedules: Sequence[Schedule]) -> Sequence[Schedule]:
        previous_hashes = await self.__get_previous_hashes(schedules)
        schedules, hashes = List.unzip(self.__get_new_schedule_hashes(schedules, previous_hashes))
        await self.__save_hashes(schedules, hashes)
        return schedules

    def __get_previous_hashes(self, schedules: Sequence[Schedule]) -> Task[Sequence[Maybe[int]]]:
        dates = List(schedules) \
            .map(self.__get_starts_at)
        return self.__schedule_hash_storage.get_hashes_by_dates(dates)

    def __get_new_schedule_hashes(self, schedules: Sequence[Schedule],
                                  previous_hashes: Sequence[Maybe[int]]) -> Sequence[tuple[Schedule, int]]:
        return List.filter_map(self.__get_new_schedule_hash, zip(schedules, previous_hashes))

    def __get_new_schedule_hash(self, t: tuple[Schedule, Maybe[int]]) -> Maybe[tuple[Schedule, int]]:
        schedule, previous_hash = t
        schedule_hash = self.__object_hashing.hash(schedule)
        return previous_hash.match(
            const(cast(Maybe[tuple[Schedule, int]], Some((schedule, schedule_hash)))),
            self.__get_new_schedule_hash_if_it_needs_to_be_stored(schedule, schedule_hash),
        )

    def __get_new_schedule_hash_if_it_needs_to_be_stored(self, schedule: Schedule, schedule_hash: int
                                                         ) -> Callable[[int], Maybe[tuple[Schedule, int]]]:
        def check_schedule_hash(previous_hash: int) -> Maybe[tuple[Schedule, int]]:
            if schedule_hash == previous_hash:
                return Nothing
            return Some((schedule, schedule_hash))

        return check_schedule_hash

    async def __save_hashes(self, schedules: Sequence[Schedule], hashes: Sequence[int]) -> None:
        dates = List(schedules) \
            .map(self.__get_starts_at)
        hashes_tuple = List.zip(dates, hashes)
        await self.__schedule_hash_storage.save(hashes_tuple)

    def __get_starts_at(self, schedule: Schedule) -> date:
        return schedule.starts_at
