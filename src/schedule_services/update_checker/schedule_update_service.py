from abc import ABCMeta, abstractmethod
from typing import (
    NoReturn,
    Awaitable,
    Sequence,
    Callable,
)

from schedule_services.schedule import (
    Schedule,
    Group,
)


class ScheduleUpdateService(metaclass=ABCMeta):
    @abstractmethod
    def start_checking_updates(self) -> Awaitable[NoReturn]: ...

    @abstractmethod
    def get_schedules(self) -> Awaitable[Sequence[Schedule]]: ...

    @abstractmethod
    def subscribe_for_updates(self, on_update: Callable[[Schedule, Sequence[Group]], None]) -> None: ...
