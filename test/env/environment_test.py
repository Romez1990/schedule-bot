from pytest import (
    fixture,
)
from unittest.mock import Mock

from src.env.environment import Environment
from src.env.environment_state_factory_interface import EnvironmentStateFactoryInterface
from src.env.environment_state import EnvironmentState


@fixture(autouse=True)
def setup() -> None:
    global env, unread_environment, read_environment
    mock_environment_state_factory: EnvironmentStateFactoryInterface = Mock()
    unread_environment = Mock()
    read_environment = Mock()
    mock_environment_state_factory.create_unread_environment = Mock(return_value=unread_environment)
    mock_environment_state_factory.create_read_environment = Mock(return_value=read_environment)
    env = Environment(mock_environment_state_factory)


env: Environment
unread_environment: EnvironmentState
read_environment: EnvironmentState

var_name = 'SOME_VAR'


def test_read_calls_unread_environment() -> None:
    unread_environment.read = Mock()
    read_environment.read = Mock()

    env.read()

    unread_environment.read.assert_called_once()
    read_environment.read.assert_not_called()


def test_read_second_time_calls_read_environment() -> None:
    unread_environment.read = Mock()
    read_environment.read = Mock()
    env.read()

    env.read()

    read_environment.read.assert_called_once()


def test_get_str_before_reading_calls_unread_environment() -> None:
    unread_environment.get_str = Mock()
    read_environment.get_str = Mock()

    env.get_str(var_name)

    unread_environment.get_str.assert_called_once()
    read_environment.get_str.assert_not_called()


def test_get_str_after_reading_calls_read_environment() -> None:
    unread_environment.get_str = Mock()
    read_environment.get_str = Mock()
    env.read()

    env.get_str(var_name)

    unread_environment.get_str.assert_not_called()
    read_environment.get_str.assert_called_once()


def test_get_bool_before_reading_calls_unread_environment() -> None:
    unread_environment.get_bool = Mock()
    read_environment.get_bool = Mock()

    env.get_bool(var_name)

    unread_environment.get_bool.assert_called_once()
    read_environment.get_bool.assert_not_called()


def test_get_bool_after_reading_calls_read_environment() -> None:
    unread_environment.get_bool = Mock()
    read_environment.get_bool = Mock()
    env.read()

    env.get_bool(var_name)

    unread_environment.get_bool.assert_not_called()
    read_environment.get_bool.assert_called_once()


def test_get_int_before_reading_calls_unread_environment() -> None:
    unread_environment.get_int = Mock()
    read_environment.get_int = Mock()

    env.get_int(var_name)

    unread_environment.get_int.assert_called_once()
    read_environment.get_int.assert_not_called()


def test_get_int_after_reading_calls_read_environment() -> None:
    unread_environment.get_int = Mock()
    read_environment.get_int = Mock()
    env.read()

    env.get_int(var_name)

    unread_environment.get_int.assert_not_called()
    read_environment.get_int.assert_called_once()


def test_get_float_before_reading_calls_unread_environment() -> None:
    unread_environment.get_float = Mock()
    read_environment.get_float = Mock()

    env.get_float(var_name)

    unread_environment.get_float.assert_called_once()
    read_environment.get_float.assert_not_called()


def test_get_float_after_reading_calls_read_environment() -> None:
    unread_environment.get_float = Mock()
    read_environment.get_float = Mock()
    env.read()

    env.get_float(var_name)

    unread_environment.get_float.assert_not_called()
    read_environment.get_float.assert_called_once()
