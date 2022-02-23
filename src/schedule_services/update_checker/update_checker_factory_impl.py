from typing import (
    NoReturn,
    Awaitable,
    Callable,
)

from infrastructure.ioc_container import service
from schedule_services.schedule import (
    Schedule,
    Group,
)
from .update_checker_factory import UpdateCheckerFactory
from .schedule_fetcher_factory import ScheduleFetcherFactory
from .update_checker import UpdateChecker
from .update_checker_impl import UpdateCheckerImpl


@service
class UpdateCheckerFactoryImpl(UpdateCheckerFactory):
    def __init__(self, schedule_fetcher_factory: ScheduleFetcherFactory) -> None:
        self.__schedule_fetcher_factory = schedule_fetcher_factory

    def create(self, on_schedules_changed: Callable[[Schedule, list[Group]], None]) -> UpdateChecker:
        return UpdateCheckerImpl(self.__schedule_fetcher_factory, on_schedules_changed)
