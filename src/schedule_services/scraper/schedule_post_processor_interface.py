from src.schedule import Schedule


class SchedulePostProcessorInterface:
    def process(self, schedule: Schedule) -> Schedule:
        raise NotImplementedError
