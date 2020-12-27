from pytest import raises

from src.immutable_collections import List


def test_eq_equal_lists_returns_true() -> None:
    list1 = List([1, 2, 3])
    list2 = List([1, 2, 3])

    result = list1 == list2

    assert result


def test_eq_different_lists_different_length_returns_false() -> None:
    list1 = List([1, 2, 3])
    list2 = List([4, 3, 2, 1])

    result = list1 == list2

    assert not result


def test_eq_different_lists_same_length_returns_false() -> None:
    list1 = List([1, 2, 3])
    list2 = List([3, 2, 1])

    result = list1 == list2

    assert not result


def test_ne_equal_lists_returns_false() -> None:
    list1 = List([1, 2, 3])
    list2 = List([1, 2, 3])

    result = list1 != list2

    assert not result


def test_ne_different_lists_different_length_returns_true() -> None:
    list1 = List([1, 2, 3])
    list2 = List([4, 3, 2, 1])

    result = list1 != list2

    assert result


def test_ne_different_lists_same_length_returns_true() -> None:
    list1 = List([1, 2, 3])
    list2 = List([3, 2, 1])

    result = list1 != list2

    assert result


def test_add_element_contains_new_element() -> None:
    old_list = List([11, 22, 33])

    new_list = old_list.add(44)

    assert 44 in new_list
    assert list(new_list).index(44) == 3
    assert len(new_list) == len(old_list) + 1


def test_remove_element_not_contain_element() -> None:
    old_list = List([11, 22, 33])

    new_list = old_list.remove(22)

    assert 22 not in new_list
    assert len(new_list) == len(old_list) - 1


def test_remove_not_existing_element_returns_same_list() -> None:
    old_list = List([11, 22, 33])

    with raises(ValueError) as e:
        old_list.remove(99)

    assert str(e.value) == '99 not in list'
