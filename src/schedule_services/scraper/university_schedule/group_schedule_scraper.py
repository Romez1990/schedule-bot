from abc import ABCMeta, abstractmethod

from data.fp.task_either import TaskEither
from schedule_services.schedule import GroupSchedule


class GroupScheduleScraper(metaclass=ABCMeta):
    @abstractmethod
    def scrap_group_schedule(self, link: str) -> TaskEither[Exception, GroupSchedule]: ...
