from pytest import (
    fixture,
    raises,
)
from unittest.mock import Mock

from src.env.read_environment import ReadEnvironment
from src.env.environment_driver import EnvironmentDriver
from src.env.errors import (
    EnvironmentAlreadyReadError,
    EnvironmentVariableNotFoundError,
    BooleanEnvironmentVariableError,
    IntegerEnvironmentVariableError,
    FloatEnvironmentVariableError,
)


@fixture(autouse=True)
def setup() -> None:
    global env, driver
    driver = Mock()
    env = ReadEnvironment(driver)


env: ReadEnvironment
driver: EnvironmentDriver

var_name = 'SOME_VAR'


def test_read_raises_error() -> None:
    with raises(EnvironmentAlreadyReadError):
        env.read()


def test_get_str_returns_value() -> None:
    driver.get_str = Mock(return_value='some value')

    value = env.get_str(var_name)

    driver.get_str.assert_called_once_with(var_name)
    assert value == 'some value'


def test_get_str_raises_not_found_error() -> None:
    driver.get_str = Mock(return_value=None)

    with raises(EnvironmentVariableNotFoundError):
        env.get_str(var_name)

    driver.get_str.assert_called_once_with(var_name)


def test_get_bool_returns_true() -> None:
    driver.get_str = Mock(return_value='true')

    value = env.get_bool(var_name)

    driver.get_str.assert_called_once_with(var_name)
    assert value is True


def test_get_bool_returns_false() -> None:
    driver.get_str = Mock(return_value='false')

    value = env.get_bool(var_name)

    driver.get_str.assert_called_once_with(var_name)
    assert value is False


def test_get_bool_raises_invalid_value_error() -> None:
    driver.get_str = Mock(return_value='another str')

    with raises(BooleanEnvironmentVariableError):
        env.get_bool(var_name)

    driver.get_str.assert_called_once_with(var_name)


def test_get_int_returns_value() -> None:
    driver.get_str = Mock(return_value='123')

    value = env.get_int(var_name)

    driver.get_str.assert_called_once_with(var_name)
    assert value == 123


def test_get_int_raises_not_number_error() -> None:
    driver.get_str = Mock(return_value='another str')

    with raises(IntegerEnvironmentVariableError):
        env.get_int(var_name)

    driver.get_str.assert_called_once_with(var_name)


def test_get_float_returns_value() -> None:
    driver.get_str = Mock(return_value='123.45')

    value = env.get_float(var_name)

    driver.get_str.assert_called_once_with(var_name)
    assert value == 123.45


def test_get_float_returns_int_value() -> None:
    driver.get_str = Mock(return_value='123')

    value = env.get_float(var_name)

    driver.get_str.assert_called_once_with(var_name)
    assert value == 123


def test_get_float_raises_not_number_error() -> None:
    driver.get_str = Mock(return_value='another str')

    with raises(FloatEnvironmentVariableError):
        env.get_float(var_name)

    driver.get_str.assert_called_once_with(var_name)
