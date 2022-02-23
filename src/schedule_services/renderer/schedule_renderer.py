from abc import ABCMeta, abstractmethod
from io import BytesIO

from schedule_services.schedule import Schedule


class ScheduleRenderer(metaclass=ABCMeta):
    @abstractmethod
    def render(self, schedule: Schedule, theme_name: str) -> BytesIO: ...
