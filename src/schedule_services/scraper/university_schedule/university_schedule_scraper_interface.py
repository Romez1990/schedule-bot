from src.schedule import Schedule


class UniversityScheduleScraperInterface:
    async def get_schedule(self) -> Schedule:
        raise NotImplementedError
