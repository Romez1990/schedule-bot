from typing import (
    Dict,
)

from src.schedule import UniversityGroup


class GroupListScraperInterface:
    async def get_groups_and_links(self) -> Dict[UniversityGroup, str]:
        raise NotImplementedError
