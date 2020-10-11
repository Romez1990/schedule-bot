from src.schedule import GroupSchedule


class GroupScheduleScraperInterface:
    async def get_group_schedule(self, group_link: str) -> GroupSchedule:
        raise NotImplementedError
