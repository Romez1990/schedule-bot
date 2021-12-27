from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
)

from data.fp.task import Task
from schedule_services.schedule import Schedule


class UniversityScheduleScraper(metaclass=ABCMeta):
    @abstractmethod
    def scrap_schedule(self) -> Task[Sequence[Schedule]]: ...
