from datetime import date
from typing import (
    Callable,
    Sequence,
    Mapping,
    cast,
)

from infrastructure.ioc_container import service
from data.fp.function import const
from data.fp.maybe import Maybe, Some, Nothing
from data.vector import List
from data.hashing import Md5ObjectHashing
from schedule_services.schedule import (
    Schedule,
    Group,
)
from .group_schedule_changes_determinant import GroupScheduleChangesDeterminant
from .group_schedule_hash_storage import GroupScheduleHashStorage


@service
class GroupScheduleChangesDeterminantImpl(GroupScheduleChangesDeterminant):
    def __init__(self, object_hashing: Md5ObjectHashing, group_schedule_hash_storage: GroupScheduleHashStorage) -> None:
        self.__object_hashing = object_hashing
        self.__group_schedule_hash_storage = group_schedule_hash_storage

    async def init(self) -> None:
        await self.__group_schedule_hash_storage.init()

    async def get_changed_groups(self, schedules: Sequence[Schedule]) -> Sequence[Schedule]:
        return []
#         previous_hashes = self.__get_previous_hashes(schedules)
#         changed_schedules_and_hashes = self.__get_new_schedule_hashes(schedules, previous_hashes)
#         if len(changed_schedules_and_hashes) == 0:
#             return schedules
#         changed_schedules, hashes = List.unzip(changed_schedules_and_hashes)
#         await self.__save_hashes(changed_schedules, hashes)
#         return changed_schedules
#
#     def __get_previous_hashes(self, schedules: Sequence[Schedule]) -> Sequence[Mapping[Group, Maybe[int]]]:
#         dates_and_groups = List(schedules) \
#             .map(self.__get_starts_at_and_groups)
#         return self.__group_schedule_hash_storage.get_hashes_by_dates(dates_and_groups)
#
#     def __get_new_schedule_hashes(self, schedules: Sequence[Schedule],
#                                   previous_hashes: Sequence[Mapping[Group, Maybe[int]]]
#                                   ) -> Sequence[tuple[Schedule, int]]:
#         return []
#         return List.filter_map(zip(schedules, previous_hashes), self.__get_new_schedule_hash)
#
#     def __get_new_schedule_hash(self, t: tuple[Schedule, Maybe[int]]) -> Maybe[tuple[Schedule, int]]:
#         schedule, previous_hash = t
#         schedule_hash = self.__object_hashing.hash(schedule)
#         return previous_hash.match(
#             const(cast(Maybe[tuple[Schedule, int]], Some((schedule, schedule_hash)))),
#             self.__get_new_schedule_hash_if_it_needs_to_be_stored(schedule, schedule_hash),
#         )
#
#     # def __get_new_schedule_hash_if_it_needs_to_be_stored(self, schedule: Schedule, schedule_hash: int
#     #                                                      ) -> Callable[[int], Maybe[tuple[Schedule, int]]]:
#     #     def check_schedule_hash(previous_hash: int) -> Maybe[tuple[Schedule, int]]:
#     #         if schedule_hash == previous_hash:
#     #             return Nothing
#     #         return Some((schedule, schedule_hash))
#     #
#     #     return check_schedule_hash
#     #
#     # async def __save_hashes(self, schedules: Sequence[Schedule], hashes: Sequence[int]) -> None:
#     #     dates = List(schedules) \
#     #         .map(self.__get_starts_at)
#     #     hashes_tuple = List.zip(dates, hashes)
#     #     await self.__group_schedule_hash_storage.save(hashes_tuple)
#
#     def __get_starts_at_and_groups(self, schedule: Schedule) -> tuple[date, Sequence[Group]]:
#         return schedule.starts_at, list(schedule)
