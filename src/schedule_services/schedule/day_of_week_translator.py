from abc import ABCMeta, abstractmethod

from .day_of_week import DayOfWeek


class DayOfWeekTranslator(metaclass=ABCMeta):
    @abstractmethod
    def translate(self, day_of_week: DayOfWeek) -> str: ...
