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


class UpdateChecker(metaclass=ABCMeta):
    @abstractmethod
    def start_checking_for_updates(self) -> Awaitable[NoReturn]: ...

    @abstractmethod
    def subscribe_to_updates(self, on_update: Callable[[Schedule, Sequence[Group]], None]) -> None: ...

    @abstractmethod
    def get_schedules(self) -> Awaitable[Sequence[Schedule]]: ...
