from returns.result import Result

from .group import Group
from .errors import GroupNameParsingError


class GroupParserInterface:
    def parse(self, group_name: str) -> Result[Group, GroupNameParsingError]:
        raise NotImplementedError
