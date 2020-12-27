from pytest import (
    fixture,
)
from returns.maybe import Nothing

from src.schedule.group_parser import GroupParser
from src.schedule import (
    Group,
    UniversityGroup,
    CollegeGroup,
    GroupNameParsingError,
)


@fixture(autouse=True)
def setup() -> None:
    global group_parser
    group_parser = GroupParser()


group_parser: GroupParser

university_group_name = 'ИС-20-Д'
college_group_name = '4ПрИн-5а.16'
not_group_name = 'not a group'


def test_parse_university_group_returns_success() -> None:
    group_result = group_parser.parse_university_group(university_group_name)

    group: UniversityGroup = group_result.unwrap()
    assert group.speciality == 'ИС'
    assert group.year == 20
    assert str(group.form) == 'Д'
    assert group.number is Nothing


def test_parse_university_group_returns_failure() -> None:
    group_result = group_parser.parse_university_group(not_group_name)

    e = group_result.failure()
    assert isinstance(e, GroupNameParsingError)
    assert str(e) == f'Cannot parse group name {not_group_name}'


def test_parse_college_group_returns_success() -> None:
    group_result = group_parser.parse_college_group(college_group_name)

    group: CollegeGroup = group_result.unwrap()
    assert group.year == 4
    assert group.speciality == 'ПрИн'
    assert group.number == 5
    assert group.a
    assert group.admission_year == 16


def test_parse_college_group_returns_failure() -> None:
    group_name = 'not a group'

    group_result = group_parser.parse_college_group(group_name)

    e = group_result.failure()
    assert isinstance(e, GroupNameParsingError)
    assert str(e) == f'Cannot parse group name {group_name}'


def test_parse_group_with_university_group_returns_success() -> None:
    group_result = group_parser.parse(university_group_name)

    group: Group = group_result.unwrap()
    assert isinstance(group, UniversityGroup)


def test_parse_group_with_college_group_returns_success() -> None:
    group_result = group_parser.parse(college_group_name)

    group: Group = group_result.unwrap()
    assert isinstance(group, CollegeGroup)


def test_parse_group_returns_failure() -> None:
    group_result = group_parser.parse(not_group_name)

    e = group_result.failure()
    assert isinstance(e, GroupNameParsingError)
    assert str(e) == f'Cannot parse group name {not_group_name}'
