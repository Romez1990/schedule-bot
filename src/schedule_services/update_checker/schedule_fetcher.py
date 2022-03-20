from abc import ABCMeta, abstractmethod
from typing import (
    NoReturn,
    Awaitable,
    Sequence,
    Callable,
)

from schedule_services.schedule import Schedule


class ScheduleFetcher(metaclass=ABCMeta):
    @abstractmethod
    def start(self) -> Awaitable[NoReturn]: ...

    @abstractmethod
    def subscribe_for_updates(self, on_schedules_fetched: Callable[[Sequence[Schedule]], None]) -> None: ...
