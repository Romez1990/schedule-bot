from .group import Group


def test_group_parse() -> None:
    group = Group('4ПрИн-5а.16')
    assert group.grade == 4
    assert group.specialty == 'ПрИн'
    assert group.number == 5
    assert group.a
    assert group.admission_year == 16
    assert str(group) == '4ПрИн-5а.16'


def test_group_parse_without_a() -> None:
    group = Group('4ПрИн-5.16')
    assert group.grade == 4
    assert group.specialty == 'ПрИн'
    assert group.number == 5
    assert not group.a
    assert group.admission_year == 16
    assert str(group) == '4ПрИн-5.16'


def test_group_parse_without_dot() -> None:
    group = Group('1ТОА-9а18')
    assert group.grade == 1
    assert group.specialty == 'ТОА'
    assert group.number == 9
    assert group.a
    assert group.admission_year == 18
    assert str(group) == '1ТОА-9а.18'


def test_group_parse_without_a_and_dot() -> None:
    group = Group('1ТОА-918')
    assert group.grade == 1
    assert group.specialty == 'ТОА'
    assert group.number == 9
    assert not group.a
    assert group.admission_year == 18
    assert str(group) == '1ТОА-9.18'


def test_group_compare() -> None:
    group1 = Group('4ПрИн-5а.16')
    group2 = Group('4ПрИн-5а.16')
    assert group1 == group2


def test_group_greater_then_year() -> None:
    group1 = Group('4ПрИн-5а.16')
    group2 = Group('3ПрИн-5а.17')
    assert group1 > group2


def test_group_greater_then_number() -> None:
    group1 = Group('4ПрИн-5а.16')
    group2 = Group('4СЭЗ-2а.16')
    assert group1 > group2


def test_group_greater_then_a() -> None:
    group1 = Group('4ПрИн-5а.16')
    group2 = Group('4ПрИн-5.16')
    assert group1 > group2


def test_group_less_then_year() -> None:
    group1 = Group('3ПрИн-5а.17')
    group2 = Group('4ПрИн-5а.16')
    assert group1 < group2


def test_group_less_then_number() -> None:
    group1 = Group('4СЭЗ-2а.16')
    group2 = Group('4ПрИн-5а.16')
    assert group1 < group2


def test_group_less_then_a() -> None:
    group1 = Group('4ПрИн-5.16')
    group2 = Group('4ПрИн-5а.16')
    assert group1 < group2
