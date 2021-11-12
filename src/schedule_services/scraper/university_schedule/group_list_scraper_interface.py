from src.schedule import UniversityGroup


class GroupListScraperInterface:
    async def get_groups_and_links(self) -> dict[UniversityGroup, str]:
        raise NotImplementedError
