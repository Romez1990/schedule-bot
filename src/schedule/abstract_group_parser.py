from returns.result import Result

from .group import Group
from .errors import GroupNameParsingException


class AbstractGroupParser:
    def parse(self, group_name: str) -> Result[Group, GroupNameParsingException]:
        raise NotImplementedError
