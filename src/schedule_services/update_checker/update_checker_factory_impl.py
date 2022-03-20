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
from .update_checker import UpdateChecker
from .update_checker_impl import UpdateCheckerImpl


@service
class UpdateCheckerFactoryImpl(UpdateCheckerFactory):
    def __init__(self, schedule_fetcher: ScheduleFetcher) -> None:
        self.__schedule_fetcher = schedule_fetcher

    def create(self, on_schedules_changed: Callable[[Schedule, Sequence[Group]], None]) -> UpdateChecker:
        return UpdateCheckerImpl(self.__schedule_fetcher, on_schedules_changed)
