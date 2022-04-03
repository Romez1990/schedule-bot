from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
    Awaitable,
)

from schedule_services.schedule import Schedule


class ScheduleChangesDeterminant(metaclass=ABCMeta):
    @abstractmethod
    def get_changed_schedules(self, schedules: Sequence[Schedule]) -> Awaitable[Sequence[Schedule]]: ...
