import pickle
from typing import (
    NoReturn,
    Awaitable,
    Callable,
    Sequence,
)

from infrastructure.ioc_container import service
from data.vector import List
from schedule_services.schedule import (
    Schedule,
    Group,
)
from .update_checker import UpdateChecker
from .schedule_fetcher_factory import ScheduleFetcherFactory


@service
class UpdateCheckerImpl(UpdateChecker):
    def __init__(self, schedule_fetcher_factory: ScheduleFetcherFactory,
                 on_schedules_changed: Callable[[Schedule, list[Group]], None]) -> None:
        self.__schedule_fetcher = schedule_fetcher_factory.create(self.__on_schedules_fetched)
        self.__on_schedule_changed = on_schedules_changed

    def start(self) -> Awaitable[NoReturn]:
        return self.__schedule_fetcher.start()

    def __on_schedules_fetched(self, schedules: Sequence[Schedule]) -> None:
        List(schedules) \
            .map(self.__schedule)

    def __schedule(self, schedule: Schedule) -> None:
        schedule_bytes = pickle.dumps(schedule)
        print(schedule_bytes)
