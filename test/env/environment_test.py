from pytest import (
    fixture,
)
from unittest.mock import Mock

from src.env.environment import Environment
from src.env.environment_state_factory_interface import EnvironmentStateFactoryInterface
from src.env.environment_state import EnvironmentState


@fixture(autouse=True)
def setup() -> None:
    global env, mock_unread_environment, mock_read_environment
    mock_environment_state_factory: EnvironmentStateFactoryInterface = Mock()
    mock_unread_environment = Mock()
    mock_read_environment = Mock()
    mock_environment_state_factory.create_unread_environment = Mock(return_value=mock_unread_environment)
    mock_environment_state_factory.create_read_environment = Mock(return_value=mock_read_environment)
    env = Environment(mock_environment_state_factory)


env: Environment
mock_unread_environment: EnvironmentState
mock_read_environment: EnvironmentState

var_name = 'SOME_VAR'


def test_read_calls_unread_environment() -> None:
    mock_unread_environment.read = Mock()
    mock_read_environment.read = Mock()

    env.read()

    mock_unread_environment.read.assert_called_once()
    mock_read_environment.read.assert_not_called()


def test_read_second_time_calls_read_environment() -> None:
    mock_unread_environment.read = Mock()
    mock_read_environment.read = Mock()
    env.read()

    env.read()

    mock_read_environment.read.assert_called_once()


def test_get_str_before_reading_calls_unread_environment() -> None:
    mock_unread_environment.get_str = Mock()
    mock_read_environment.get_str = Mock()

    env.get_str(var_name)

    mock_unread_environment.get_str.assert_called_once()
    mock_read_environment.get_str.assert_not_called()


def test_get_str_after_reading_calls_read_environment() -> None:
    mock_unread_environment.get_str = Mock()
    mock_read_environment.get_str = Mock()
    env.read()

    env.get_str(var_name)

    mock_unread_environment.get_str.assert_not_called()
    mock_read_environment.get_str.assert_called_once()


def test_get_bool_before_reading_calls_unread_environment() -> None:
    mock_unread_environment.get_bool = Mock()
    mock_read_environment.get_bool = Mock()

    env.get_bool(var_name)

    mock_unread_environment.get_bool.assert_called_once()
    mock_read_environment.get_bool.assert_not_called()


def test_get_bool_after_reading_calls_read_environment() -> None:
    mock_unread_environment.get_bool = Mock()
    mock_read_environment.get_bool = Mock()
    env.read()

    env.get_bool(var_name)

    mock_unread_environment.get_bool.assert_not_called()
    mock_read_environment.get_bool.assert_called_once()


def test_get_int_before_reading_calls_unread_environment() -> None:
    mock_unread_environment.get_int = Mock()
    mock_read_environment.get_int = Mock()

    env.get_int(var_name)

    mock_unread_environment.get_int.assert_called_once()
    mock_read_environment.get_int.assert_not_called()


def test_get_int_after_reading_calls_read_environment() -> None:
    mock_unread_environment.get_int = Mock()
    mock_read_environment.get_int = Mock()
    env.read()

    env.get_int(var_name)

    mock_unread_environment.get_int.assert_not_called()
    mock_read_environment.get_int.assert_called_once()


def test_get_float_before_reading_calls_unread_environment() -> None:
    mock_unread_environment.get_float = Mock()
    mock_read_environment.get_float = Mock()

    env.get_float(var_name)

    mock_unread_environment.get_float.assert_called_once()
    mock_read_environment.get_float.assert_not_called()


def test_get_float_after_reading_calls_read_environment() -> None:
    mock_unread_environment.get_float = Mock()
    mock_read_environment.get_float = Mock()
    env.read()

    env.get_float(var_name)

    mock_unread_environment.get_float.assert_not_called()
    mock_read_environment.get_float.assert_called_once()
