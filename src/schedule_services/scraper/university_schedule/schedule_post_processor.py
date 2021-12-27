from abc import ABCMeta, abstractmethod

from schedule_services.schedule import Schedule


class SchedulePostProcessor(metaclass=ABCMeta):
    @abstractmethod
    def process(self, schedule: Schedule) -> Schedule: ...
