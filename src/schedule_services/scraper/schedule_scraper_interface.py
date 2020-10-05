from src.schedule import Schedule


class ScheduleScraperInterface:
    async def get_schedule(self) -> Schedule:
        raise NotImplementedError
