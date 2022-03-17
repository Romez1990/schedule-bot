from pytest import raises

from data.vector import List


def test_eq__equal_lists__returns_true() -> None:
    list1 = List([1, 2, 3])
    list2 = List([1, 2, 3])

    result = list1 == list2

    assert result


def test_eq__different_lists_different_length__returns_false() -> None:
    list1 = List([1, 2, 3])
    list2 = List([4, 3, 2, 1])

    result = list1 == list2

    assert not result


def test_eq__different_lists_same_length__returns_false() -> None:
    list1 = List([1, 2, 3])
    list2 = List([3, 2, 1])

    result = list1 == list2

    assert not result


def test_ne__equal_lists_returns__false() -> None:
    list1 = List([1, 2, 3])
    list2 = List([1, 2, 3])

    result = list1 != list2

    assert not result


def test_ne__different_lists_different_length__returns_true() -> None:
    list1 = List([1, 2, 3])
    list2 = List([4, 3, 2, 1])

    result = list1 != list2

    assert result


def test_ne__different_lists_same_length__returns_true() -> None:
    list1 = List([1, 2, 3])
    list2 = List([3, 2, 1])

    result = list1 != list2

    assert result


def test_add__element__contains_new_element() -> None:
    old_list = List([11, 22, 33])

    new_list = old_list.add(44)

    assert 44 in new_list
    assert list(new_list).index(44) == 3
    assert len(new_list) == len(old_list) + 1
