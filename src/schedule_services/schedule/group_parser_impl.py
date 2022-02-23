# from re import (
#     Match,
#     compile as compile_regex,
# )
# from typing import (
#     Callable,
#     TypeVar,
# )
#
# from infrastructure.ioc_container import service
# from data.fp.maybe import Maybe, Some, Nothing
# from data.fp.either import Either, Right, Left
# from data.vector import List, lazy_reduce
# from .group_parser import GroupParser
# from .group import Group
# from .university_group import UniversityGroup
# from .college_group import CollegeGroup
# from .errors import GroupNameParsingError
#
# T = TypeVar('T', bound=Group)
#
#
# @service
# class GroupParserImpl(GroupParser):
#     def __init__(self) -> None:
#         self.__university_group_regex = compile_regex(
#             '^(?P<specialty>[А-Яа-я]{2,3})-(?P<year>\\d{2})-(?P<form>[А-Яа-я]{1,2})(?P<number>\\d?)$')
#         self.__college_group_regex = compile_regex(
#             '^(?P<year>[1-4])(?P<specialty>[А-Яа-я]{2,4})-(?P<number>\\d{1,2})(?P<a>а?)\\.?(?P<admission_year>\\d{2})$')
#
#     def parse(self, group_name: str) -> Either[Group, GroupNameParsingError]:
#         parsers: List[Callable[[], Either[Group, GroupNameParsingError]]] = List([
#             lambda: self.parse_university_group(group_name),
#             lambda: self.parse_college_group(group_name),
#         ])
#         return lazy_reduce(self.__rescue, parsers)
#
#     def __rescue(
#             self,
#             group_result: Either[Group, GroupNameParsingError],
#             get_next_group: Callable[[], Either[Group, GroupNameParsingError]],
#     ) -> Either[Group, GroupNameParsingError]:
#         return group_result.lash(lambda _: get_next_group())
#
#     def parse_university_group(self, group_name: str) -> Either[UniversityGroup, GroupNameParsingError]:
#         match = self.__university_group_regex.search(group_name)
#         maybe_group = Maybe.from_optional(match) \
#             .map(self.__create_university_group)
#         return self.__maybe_to_result(group_name, maybe_group)
#
#     def parse_college_group(self, group_name: str) -> Either[CollegeGroup, GroupNameParsingError]:
#         match = self.__college_group_regex.search(group_name)
#         maybe_group = Maybe.from_optional(match) \
#             .map(self.__create_college_group)
#         return self.__maybe_to_result(group_name, maybe_group)
#
#     def __create_university_group(self, match: Match) -> UniversityGroup:
#         return UniversityGroup(
#             match.group('specialty'),
#             int(match.group('year')),
#             match.group('form'),
#             self.__parse_number(match.group('number')),
#         )
#
#     def __create_college_group(self, match: Match) -> CollegeGroup:
#         return CollegeGroup(
#             int(match.group('year')),
#             match.group('specialty'),
#             int(match.group('number')),
#             int(match.group('year')),
#             match.group('specialty'),
#             int(match.group('number')),
#             bool(match.group('a')),
#             int(match.group('admission_year')),
#         )
#
#     def __parse_number(self, number: str) -> Maybe[int]:
#         return Some(int(number)) if number != '' else Nothing
#
#     def __maybe_to_result(self, group_name: str, maybe_group: Maybe[T]) -> Either[T, GroupNameParsingError]:
#         return Right(maybe_group.get_or_raise()) if maybe_group != Nothing else Left(GroupNameParsingError(group_name))
