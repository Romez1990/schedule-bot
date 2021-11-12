from returns.result import Result

from .group import Group
from .university_group import UniversityGroup
from .college_group import CollegeGroup
from .errors import GroupNameParsingError


class GroupParserInterface:
    def parse(self, group_name: str) -> Result[Group, GroupNameParsingError]:
        raise NotImplementedError

    def parse_university_group(self, group_name: str) -> Result[UniversityGroup, GroupNameParsingError]:
        raise NotImplementedError

    def parse_college_group(self, group_name: str) -> Result[CollegeGroup, GroupNameParsingError]:
        raise NotImplementedError
