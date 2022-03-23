from asyncio import create_task
from typing import (
    Callable,
    Sequence,
)

from infrastructure.ioc_container import service
from data.fp.task import Task
from data.vector import List
from schedule_services.schedule import (
    Schedule,
    Group,
)
from .update_checker import UpdateChecker
from .schedule_fetcher import ScheduleFetcher
from .schedule_hashing import ScheduleHashing
from .schedule_hash_storage import ScheduleHashStorage


@service
class UpdateCheckerImpl(UpdateChecker):
    def __init__(self, schedule_fetcher: ScheduleFetcher, schedule_hashing: ScheduleHashing,
                 schedule_hash_storage: ScheduleHashStorage,
                 on_schedules_changed: Callable[[Schedule, Sequence[Group]], None]) -> None:
        schedule_fetcher.subscribe_for_updates(self.__on_schedules_fetched)
        self.__schedule_hashing = schedule_hashing
        self.__schedule_hash_storage = schedule_hash_storage
        self.__on_schedule_changed = on_schedules_changed

    def __on_schedules_fetched(self, schedules: Sequence[Schedule]) -> None:
        tasks = List(schedules) \
            .map(self.__check_schedule)
        task = Task.parallel(tasks)
        create_task(task)

    def __check_schedule(self, schedule: Schedule) -> Task[None]:
        schedule_hash = self.__schedule_hashing.hash(schedule)
        return self.__schedule_hash_storage.get_hash_by_date(schedule.starts_at) \
            .match_awaitable(self.__store_schedule_hash(schedule, schedule_hash),
                             self.__check_schedule_hash(schedule, schedule_hash))

    def __store_schedule_hash(self, schedule: Schedule, schedule_hash: int) -> Callable[[], Task[None]]:
        def store_schedule_hash() -> Task[None]:
            return self.__schedule_hash_storage.save(schedule.starts_at, schedule_hash)

        return store_schedule_hash

    def __check_schedule_hash(self, schedule: Schedule, schedule_hash: int) -> Callable[[int], Task[None]]:
        def check_schedule_hash(stored_schedule_hash: int) -> Task[None]:
            if schedule_hash == stored_schedule_hash:
                return Task.from_value(None)

            return self.__schedule_hash_storage.update_schedule_hash(schedule.starts_at, schedule_hash) \
                .map(self.__check_day_schedules(schedule))

        return check_schedule_hash

    def __check_day_schedules(self, schedule: Schedule) -> Callable[[None], None]:
        def check_day_schedules(_: None) -> None:
            groups = self.__get_changed_groups()
            self.__on_schedule_changed(schedule, groups)

        return check_day_schedules

    def __get_changed_groups(self) -> Sequence[Group]:
        ...
