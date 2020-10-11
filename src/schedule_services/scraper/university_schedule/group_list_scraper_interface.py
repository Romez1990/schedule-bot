from typing import (
    Dict,
)

from src.schedule import Group


class GroupListScraperInterface:
    async def get_groups_and_links(self) -> Dict[Group, str]:
        raise NotImplementedError
