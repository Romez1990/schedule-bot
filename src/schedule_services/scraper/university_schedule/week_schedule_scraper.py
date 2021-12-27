from abc import ABCMeta, abstractmethod

from data.fp.task_either import TaskEither
from schedule_services.schedule import WeekSchedule


class WeekScheduleScraper(metaclass=ABCMeta):
    @abstractmethod
    def scrap_week_schedule(self, link: str) -> TaskEither[Exception, WeekSchedule]: ...
