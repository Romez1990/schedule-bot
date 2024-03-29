from abc import ABCMeta, abstractmethod
from typing import (
    NoReturn,
    Awaitable,
    Sequence,
    Callable,
)

from schedule_services.schedule import (
    Schedule,
)


class ScheduleUpdateService(metaclass=ABCMeta):
    @abstractmethod
    def subscribe_to_updates(self, on_update: Callable[[Sequence[Schedule]], None]) -> None: ...

    @abstractmethod
    def init(self) -> Awaitable[None]: ...

    @abstractmethod
    def start_checking_for_updates(self) -> Awaitable[NoReturn]: ...

    @abstractmethod
    def get_schedules(self) -> Sequence[Schedule]: ...
