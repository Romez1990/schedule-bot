from typing import (
    Sequence,
    Callable,
)

from infrastructure.ioc_container import service
from schedule_services.schedule import (
    Schedule,
    Group,
)
from .update_checker_factory import UpdateCheckerFactory
from .schedule_fetcher import ScheduleFetcher
from .schedule_hashing import ScheduleHashing
from .schedule_hash_storage import ScheduleHashStorage
from .update_checker import UpdateChecker
from .update_checker_impl import UpdateCheckerImpl


@service
class UpdateCheckerFactoryImpl(UpdateCheckerFactory):
    def __init__(self, schedule_fetcher: ScheduleFetcher, schedule_hashing: ScheduleHashing,
                 schedule_hash_storage: ScheduleHashStorage) -> None:
        self.__schedule_fetcher = schedule_fetcher
        self.__schedule_hashing = schedule_hashing
        self.__schedule_hash_storage = schedule_hash_storage

    def create(self, on_schedules_changed: Callable[[Schedule, Sequence[Group]], None]) -> UpdateChecker:
        return UpdateCheckerImpl(self.__schedule_fetcher, self.__schedule_hashing, self.__schedule_hash_storage,
                                 on_schedules_changed)
