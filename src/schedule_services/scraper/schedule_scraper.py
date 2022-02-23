from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
)

from data.fp.task import Task
from schedule_services.schedule import Schedule


class ScheduleScraper(metaclass=ABCMeta):
    @abstractmethod
    def scrap_schedules(self) -> Task[Sequence[Schedule]]: ...
