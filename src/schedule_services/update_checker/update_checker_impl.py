import pickle
from typing import (
    NoReturn,
    Awaitable,
    Callable,
    Sequence,
)

from infrastructure.ioc_container import service
from data.vector import List
from data.serializers import BytesSerializer
from data.hashing import Md5Hashing
from schedule_services.schedule import (
    Schedule,
    Group,
)
from .update_checker import UpdateChecker
from .schedule_fetcher_factory import ScheduleFetcherFactory


@service
class UpdateCheckerImpl(UpdateChecker):
    def __init__(self, schedule_fetcher_factory: ScheduleFetcherFactory, bytes_serializer: BytesSerializer,
                 md5_hashing: Md5Hashing, on_schedules_changed: Callable[[Schedule, list[Group]], None]) -> None:
        self.__schedule_fetcher = schedule_fetcher_factory.create(self.__on_schedules_fetched)
        self.__bytes_serializer = bytes_serializer
        self.__md5_hashing = md5_hashing
        self.__on_schedule_changed = on_schedules_changed

    def start(self) -> Awaitable[NoReturn]:
        return self.__schedule_fetcher.start()

    def __on_schedules_fetched(self, schedules: Sequence[Schedule]) -> None:
        List(schedules) \
            .map(self.__schedule)

    def __schedule(self, schedule: Schedule) -> None:
        schedule_bytes = self.__bytes_serializer.serialize(schedule)
        schedule_hash = self.__md5_hashing.hash(schedule_bytes)
