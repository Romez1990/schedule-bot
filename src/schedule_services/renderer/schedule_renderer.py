from io import BytesIO

from src.schedule import (
    Schedule,
)
from .schedule_renderer_interface import ScheduleRendererInterface


class ScheduleRenderer(ScheduleRendererInterface):
    def render(self, schedule: Schedule, theme_name: str) -> BytesIO:
        pass
