from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
    Awaitable,
)

from schedule_services.schedule import (
    Schedule,
)


class GroupScheduleChangesDeterminant(metaclass=ABCMeta):
    @abstractmethod
    def init(self) -> Awaitable[None]: ...

    @abstractmethod
    def get_changed_groups(self, schedules: Sequence[Schedule]) -> Awaitable[Sequence[Schedule]]: ...
