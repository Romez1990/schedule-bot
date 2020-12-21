from functools import reduce
from re import search, Match
from typing import (
    List,
    Callable,
    TypeVar,
)
from returns.maybe import Maybe, Some, Nothing
from returns.result import Result, Success, Failure

from .group_parser_interface import GroupParserInterface
from .group import Group
from .university_group import UniversityGroup
from .college_group import CollegeGroup
from .errors import GroupNameParsingError

T = TypeVar('T', bound=Group)


class GroupParser(GroupParserInterface):
    def parse(self, group_name: str) -> Result[Group, GroupNameParsingError]:
        parsers: List[Callable[[], Result[Group, GroupNameParsingError]]] = [
            lambda: self.parse_university_group(group_name),
            lambda: self.parse_college_group(group_name),
        ]
        return reduce(self.__rescue, parsers[1:], parsers[0]())

    def __rescue(
            self,
            group_result: Result[Group, GroupNameParsingError],
            get_next_group: Callable[[], Result[Group, GroupNameParsingError]],
    ) -> Result[Group, GroupNameParsingError]:
        return group_result.lash(lambda _: get_next_group())

    def parse_university_group(self, group_name: str) -> Result[UniversityGroup, GroupNameParsingError]:
        match = search(
            '^(?P<specialty>[А-Яа-я]{2,3})-(?P<year>\\d{2})-(?P<form>[А-Яа-я]{1,2})(?P<number>\\d?)$',
            group_name)
        maybe_group = Maybe.from_optional(match) \
            .map(self.__create_university_group)
        return self.__maybe_to_result(group_name, maybe_group)

    def parse_college_group(self, group_name: str) -> Result[CollegeGroup, GroupNameParsingError]:
        match = search(
            '^(?P<year>[1-4])(?P<specialty>[А-Яа-я]{2,4})-(?P<number>\\d{1,2})(?P<a>а?)\\.?(?P<admission_year>\\d{2})$',
            group_name)
        maybe_group = Maybe.from_optional(match) \
            .map(self.__create_college_group)
        return self.__maybe_to_result(group_name, maybe_group)

    def __create_university_group(self, match: Match) -> UniversityGroup:
        return UniversityGroup(
            match.group('specialty'),
            int(match.group('year')),
            match.group('form'),
            self.__parse_number(match.group('number')),
        )

    def __create_college_group(self, match: Match) -> CollegeGroup:
        return CollegeGroup(
            int(match.group('year')),
            match.group('specialty'),
            int(match.group('number')),
            bool(match.group('a')),
            int(match.group('admission_year')),
        )

    def __parse_number(self, number: str) -> Maybe[int]:
        return Some(int(number)) if number != '' else Nothing

    def __maybe_to_result(self, group_name: str, maybe_group: Maybe[T]) -> Result[T, GroupNameParsingError]:
        return Success(maybe_group.unwrap()) if maybe_group != Nothing else Failure(GroupNameParsingError(group_name))
