from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Sequence,
)

from schedule_services.schedule import Schedule
from .schedule_fetcher import ScheduleFetcher


class ScheduleFetcherFactory(metaclass=ABCMeta):
    @abstractmethod
    def create(self, on_schedules_fetched: Callable[[Sequence[Schedule]], None]) -> ScheduleFetcher: ...
