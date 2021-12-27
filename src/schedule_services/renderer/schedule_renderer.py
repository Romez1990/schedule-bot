from io import BytesIO

from schedule_services.schedule import Schedule


class ScheduleRenderer:
    def render(self, schedule: Schedule, theme_name: str) -> BytesIO:
        raise NotImplementedError
