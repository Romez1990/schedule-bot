from functools import reduce
from re import search, Match
from typing import (
    List,
    Callable,
)
from returns.maybe import Maybe, Some, Nothing
from returns.result import Result, Success, Failure

from .abstract_group_parser import AbstractGroupParser
from .group import Group
from .university_group import UniversityGroup
from .college_group import CollegeGroup
from .errors import GroupNameParsingException


class GroupParser(AbstractGroupParser):
    def parse(self, group_name: str) -> Result[Group, GroupNameParsingException]:
        parsers: List[Callable[[], Maybe[Group]]] = [
            lambda: self.__parse_university_group(group_name),
            lambda: self.__parse_college_group(group_name),
        ]
        group = reduce(self.__rescue, parsers, Nothing)
        return Success(group.unwrap()) if group != Nothing else Failure(GroupNameParsingException(group_name))

    def __rescue(self, group: Maybe[Group], get_next_group: Callable[[], Maybe[Group]]) -> Maybe[Group]:
        return group if group != Nothing else get_next_group()

    def __parse_university_group(self, group_name: str) -> Maybe[UniversityGroup]:
        return Maybe.from_value(
            search(
                '^(?P<specialty>[А-Яа-я]{2,3})-(?P<year>\\d{2})-(?P<form>[А-Яа-я]{1,2})(?P<number>\\d?)$',
                group_name)) \
            .map(self.__create_university_group)

    def __parse_college_group(self, group_name: str) -> Maybe[CollegeGroup]:
        return Maybe.from_value(
            search(
                '^(?P<year>[1-4])(?P<specialty>[А-Яа-я]{2,4})-(?P<number>\\d{1,2})(?P<a>а?)\\.?'
                '(?P<admission_year>\\d{2})$',
                group_name)) \
            .map(self.__create_college_group)

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
