from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
)

from schedule_services.schedule import (
    Schedule,
    Group,
)
from .update_checker import UpdateChecker


class UpdateCheckerFactory(metaclass=ABCMeta):
    @abstractmethod
    def create(self, on_schedules_changed: Callable[[Schedule, list[Group]], None]) -> UpdateChecker: ...
