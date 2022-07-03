from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
    Awaitable,
)

from schedule_services.schedule import (
    Schedule,
)


class ScheduleUpdateFetcher(metaclass=ABCMeta):
    @abstractmethod
    def init(self) -> Awaitable[None]: ...

    @abstractmethod
    def fetch_updates(self) -> Awaitable[tuple[Sequence[Schedule], Sequence[Schedule]]]: ...
