from pytest import raises

from data.vector import Dict


def test_eq__equal_dicts__returns_true() -> None:
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


def test_eq__different_dicts_different_length__returns_false() -> None:
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


def test_eq__different_dicts_same_length_with_different_keys__returns_false() -> None:
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


def test_eq__different_dicts_with_same_keys_and_different_values__returns_false() -> None:
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


def test_ne__equal_dicts__returns_true() -> None:
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


def test_ne__different_dicts_different_length__returns_false() -> None:
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


def test_ne__different_dicts_same_length_with_different_keys__returns_false() -> None:
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


def test_ne__different_dicts_with_same_keys_and_different_values__returns_false() -> None:
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


def test_add__element__contains_new_element() -> None:
    old_dict = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })

    new_dict = old_dict.add('dd', 44)

    assert 'dd' in new_dict
    assert new_dict['dd'] == 44
    assert len(new_dict) == len(old_dict) + 1


def test_remove__element__not_contain_element() -> None:
    old_dict = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })

    new_dict = old_dict.remove('b')

    assert 'b' not in new_dict
    assert len(new_dict) == len(old_dict) - 1


def test_remove__not_existing_element__raises_error() -> None:
    old_dict = Dict({
        'a': 11,
        'b': 22,
        'c': 33,
    })

    with raises(KeyError) as e:
        old_dict.remove('z')

    assert str(e.value) == '\'z\''
