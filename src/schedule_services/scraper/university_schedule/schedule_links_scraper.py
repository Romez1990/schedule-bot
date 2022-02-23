from abc import ABCMeta, abstractmethod
from typing import (
    Sequence,
)

from data.fp.task_either import TaskEither
from schedule_services.schedule import ScheduleLinks


class ScheduleLinksScraper(metaclass=ABCMeta):
    @abstractmethod
    def scrap_schedules_links(self) -> TaskEither[Exception, Sequence[ScheduleLinks]]: ...
