# from abc import ABCMeta, abstractmethod
#
# from data.fp.either import Either
# from .group import Group
# from .university_group import UniversityGroup
# from .college_group import CollegeGroup
# from .errors import GroupNameParsingError
#
#
# class GroupParser(metaclass=ABCMeta):
#     @abstractmethod
#     def parse(self, group_name: str) -> Either[Group, GroupNameParsingError]: ...
#
#     @abstractmethod
#     def parse_university_group(self, group_name: str) -> Either[UniversityGroup, GroupNameParsingError]: ...
#
#     @abstractmethod
#     def parse_college_group(self, group_name: str) -> Either[CollegeGroup, GroupNameParsingError]: ...
