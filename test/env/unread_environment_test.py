from pytest import (
    fixture,
    raises,
)
from unittest.mock import Mock

from src.env.unread_environment import UnreadEnvironment
from src.env.environment_driver import EnvironmentDriver
from src.env.errors import EnvironmentUnreadError


@fixture(autouse=True)
def setup() -> None:
    global env, driver
    driver = Mock()
    env = UnreadEnvironment(driver)


env: UnreadEnvironment
driver: EnvironmentDriver

var_name = 'SOME_VAR'


def test_read_calls_driver() -> None:
    driver.read = Mock()

    env.read()

    driver.read.assert_called_once()


def test_get_str_raises_error() -> None:
    with raises(EnvironmentUnreadError):
        env.get_str(var_name)


def test_get_bool_raises_error() -> None:
    with raises(EnvironmentUnreadError):
        env.get_bool(var_name)


def test_get_int_raises_error() -> None:
    with raises(EnvironmentUnreadError):
        env.get_int(var_name)


def test_get_float_raises_error() -> None:
    with raises(EnvironmentUnreadError):
        env.get_float(var_name)
