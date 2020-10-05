from src.schedule import Schedule
from .primitives import RenderScheme


class ScheduleTransformerInterface:
    def transform(self, schedule: Schedule) -> RenderScheme:
        raise NotImplementedError
