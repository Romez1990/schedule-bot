from io import BytesIO

from src.schedule import (
    Schedule,
)
from .schedule_renderer_interface import ScheduleRendererInterface
from .schedule_transformer_interface import ScheduleTransformerInterface


class ScheduleRenderer(ScheduleRendererInterface):
    def __init__(self, transformer: ScheduleTransformerInterface) -> None:
        self.__transformer = transformer

    def render(self, schedule: Schedule, theme_name: str) -> BytesIO:
        scheme = self.__transformer.transform(schedule)
