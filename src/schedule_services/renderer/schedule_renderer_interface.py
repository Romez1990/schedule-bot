from io import BytesIO

from src.schedule import Schedule


class ScheduleRendererInterface:
    def render(self, schedule: Schedule, theme_name: str) -> BytesIO:
        raise NotImplementedError
