from pytest import raises

from src.immutable_collections import Dict


def test_eq_equal_dicts_returns_true() -> None:
    dict1 = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })
    dict2 = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })

    result = dict1 == dict2

    assert result


def test_eq_different_dicts_different_length_returns_false() -> None:
    dict1 = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })
    dict2 = Dict({
        'z': 44,
        'y': 33,
        'x': 22,
        'w': 11,
    })

    result = dict1 == dict2

    assert not result


def test_eq_different_dicts_same_length_with_different_keys_returns_false() -> None:
    dict1 = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })
    dict2 = Dict({
        'z': 33,
        'y': 22,
        'x': 11,
    })

    result = dict1 == dict2

    assert not result


def test_eq_different_dicts_with_same_keys_and_different_values_returns_false() -> None:
    dict1 = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })
    dict2 = Dict({
        'a': 33,
        'b': 22,
        'c': 11,
    })

    result = dict1 == dict2

    assert not result


def test_ne_equal_dicts_returns_true() -> None:
    dict1 = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })
    dict2 = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })

    result = dict1 != dict2

    assert not result


def test_ne_different_dicts_different_length_returns_false() -> None:
    dict1 = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })
    dict2 = Dict({
        'z': 44,
        'y': 33,
        'x': 22,
        'w': 11,
    })

    result = dict1 != dict2

    assert result


def test_ne_different_dicts_same_length_with_different_keys_returns_false() -> None:
    dict1 = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })
    dict2 = Dict({
        'z': 33,
        'y': 22,
        'x': 11,
    })

    result = dict1 != dict2

    assert result


def test_ne_different_dicts_with_same_keys_and_different_values_returns_false() -> None:
    dict1 = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })
    dict2 = Dict({
        'a': 33,
        'b': 22,
        'c': 11,
    })

    result = dict1 != dict2

    assert result


def test_add_element_contains_new_element() -> None:
    old_dict = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })

    new_dict = old_dict.add('dd', 44)

    assert 'dd' in new_dict
    assert new_dict['dd'] == 44
    assert len(new_dict) == len(old_dict) + 1


def test_remove_element_not_contain_element() -> None:
    old_dict = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })

    new_dict = old_dict.remove('b')

    assert 'b' not in new_dict
    assert len(new_dict) == len(old_dict) - 1


def test_remove_not_existing_element_returns_same_dict() -> None:
    old_dict = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })

    with raises(KeyError) as e:
        old_dict.remove('z')

    assert str(e.value) == '\'z\''
