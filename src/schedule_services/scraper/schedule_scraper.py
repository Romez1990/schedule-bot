from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
)

from data.fp.task_either import TaskEither
from schedule_services.schedule import Schedule


class ScheduleScraper(metaclass=ABCMeta):
    @abstractmethod
    def scrap_schedule(self) -> TaskEither[Exception, Sequence[Schedule]]: ...
