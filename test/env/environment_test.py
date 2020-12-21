from pytest import (
    fixture,
    raises,
)
from unittest.mock import Mock

from src.env.environment import Environment
from src.env.environment_driver import EnvironmentDriver


@fixture(autouse=True)
def setup() -> None:
    global env, mock_driver
    mock_driver = Mock()
    env = Environment(mock_driver)


env: Environment
mock_driver: EnvironmentDriver

var_name = 'SOME_VAR'


def test_read() -> None:
    mock_driver.read = Mock()

    env.read()

    mock_driver.read.assert_called_once()


def test_read_error() -> None:
    with raises(EnvironmentError) as e:
        env.get_str(var_name)

    assert str(e.value) == 'environment was not read'


def test_get_str_returns_value() -> None:
    mock_driver.get_str = Mock(return_value='some value')

    env.read()
    value = env.get_str(var_name)

    mock_driver.get_str.assert_called_once_with(var_name)
    assert value == 'some value'


def test_get_str_raises_not_found_error() -> None:
    mock_driver.get_str = Mock(return_value=None)

    env.read()
    with raises(EnvironmentError) as e:
        env.get_str(var_name)

    assert str(e.value) == f'no {var_name} environment variable'
    mock_driver.get_str.assert_called_once_with(var_name)


def test_get_bool_returns_true() -> None:
    mock_driver.get_str = Mock(return_value='true')

    env.read()
    value = env.get_bool(var_name)

    mock_driver.get_str.assert_called_once_with(var_name)
    assert value is True


def test_get_bool_returns_false() -> None:
    mock_driver.get_str = Mock(return_value='false')

    env.read()
    value = env.get_bool(var_name)

    mock_driver.get_str.assert_called_once_with(var_name)
    assert value is False


def test_get_bool_raises_invalid_value_error() -> None:
    mock_driver.get_str = Mock(return_value='another str')

    env.read()
    with raises(EnvironmentError) as e:
        env.get_bool(var_name)

    mock_driver.get_str.assert_called_once_with(var_name)
    assert str(e.value) == f'key {var_name} can only be true or false'


def test_get_int_returns_value() -> None:
    mock_driver.get_str = Mock(return_value='123')

    env.read()
    value = env.get_int(var_name)

    mock_driver.get_str.assert_called_once_with(var_name)
    assert value == 123


def test_get_int_raises_not_number_error() -> None:
    mock_driver.get_str = Mock(return_value='another str')

    env.read()
    with raises(EnvironmentError) as e:
        env.get_int(var_name)

    mock_driver.get_str.assert_called_once_with(var_name)
    assert str(e.value) == f'key {var_name} must be int'


def test_get_float_returns_value() -> None:
    mock_driver.get_str = Mock(return_value='123.45')

    env.read()
    value = env.get_float(var_name)

    mock_driver.get_str.assert_called_once_with(var_name)
    assert value == 123.45


def test_get_float_returns_int_value() -> None:
    mock_driver.get_str = Mock(return_value='123')

    env.read()
    value = env.get_float(var_name)

    mock_driver.get_str.assert_called_once_with(var_name)
    assert value == 123


def test_get_float_raises_not_number_error() -> None:
    mock_driver.get_str = Mock(return_value='another str')

    env.read()
    with raises(EnvironmentError) as e:
        env.get_float(var_name)

    mock_driver.get_str.assert_called_once_with(var_name)
    assert str(e.value) == f'key {var_name} must be float'
