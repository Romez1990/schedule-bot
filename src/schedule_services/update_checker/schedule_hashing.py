from abc import ABCMeta, abstractmethod

from schedule_services.schedule import (
    Schedule,
    DaySchedule,
)


class ScheduleHashing(metaclass=ABCMeta):
    @abstractmethod
    def hash(self, schedule: Schedule | DaySchedule) -> int: ...
