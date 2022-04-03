from pytest import (
    fixture,
    raises,
    mark,
)
from unittest.mock import Mock

from infrastructure.env import (
    EnvImpl,
    EnvReader,
)
from infrastructure.env.errors import (
    EnvironmentVariableNotFoundError,
    EnvironmentVariableIsEmptyError,
    BooleanEnvironmentVariableError,
    IntegerEnvironmentVariableError,
    PositiveIntegerEnvironmentVariableError,
    FloatEnvironmentVariableError,
    PositiveFloatEnvironmentVariableError,
)


@fixture(autouse=True)
def setup() -> None:
    global env, env_reader
    env_reader = Mock()
    env = EnvImpl(env_reader)


env: EnvImpl
env_reader: EnvReader

var_name = 'SOME_VAR'


def test_get_str__when_value_exists__returns_value() -> None:
    value = 'some value'
    env_reader.get_str = Mock(return_value=value)

    result = env.get_str(var_name)

    env_reader.get_str.assert_called_once_with(var_name)
    assert result is value


def test_get_str__when_value_does_not_exist__raises_error() -> None:
    env_reader.get_str = Mock(return_value=None)

    with raises(EnvironmentVariableNotFoundError):
        env.get_str(var_name)

    env_reader.get_str.assert_called_once_with(var_name)


def test_get_str__when_value_is_empty__raises_error() -> None:
    env_reader.get_str = Mock(return_value='')

    with raises(EnvironmentVariableIsEmptyError):
        env.get_str(var_name)

    env_reader.get_str.assert_called_once_with(var_name)


@mark.parametrize('input_value, bool_value', [('true', True), ('false', False)])
def test_get_bool__when_value_is_valid__returns_bool(input_value: str, bool_value: bool) -> None:
    env_reader.get_str = Mock(return_value=input_value)

    result = env.get_bool(var_name)

    env_reader.get_str.assert_called_once_with(var_name)
    assert result == bool_value


def test_get_bool__when_value_is_invalid__raises_error() -> None:
    env_reader.get_str = Mock(return_value='not bool value')

    with raises(BooleanEnvironmentVariableError):
        env.get_bool(var_name)

    env_reader.get_str.assert_called_once_with(var_name)


@mark.parametrize('input_value, int_value', [('3', 3), ('123', 123), ('-254', -254), ('0', 0), ('-0', 0)])
def test_get__int_when_value_is_valid__returns_int(input_value: str, int_value: bool) -> None:
    env_reader.get_str = Mock(return_value=input_value)

    result = env.get_int(var_name)

    env_reader.get_str.assert_called_once_with(var_name)
    assert result == int_value


def test_get_int__when_value_is_invalid__raises_error() -> None:
    env_reader.get_str = Mock(return_value='not int value')

    with raises(IntegerEnvironmentVariableError):
        env.get_int(var_name)

    env_reader.get_str.assert_called_once_with(var_name)


@mark.parametrize('input_value, int_value', [('3', 3), ('123', 123), ('254', 254)])
def test_get_positive_int__when_value_is_valid__returns_int(input_value: str, int_value: bool) -> None:
    env_reader.get_str = Mock(return_value=input_value)

    result = env.get_positive_int(var_name)

    env_reader.get_str.assert_called_once_with(var_name)
    assert result == int_value


@mark.parametrize('input_value', ['-3', '-123', '-254', '0', '-0'])
def test_get_positive_int__when_value_is_invalid__raises_error(input_value: str) -> None:
    env_reader.get_str = Mock(return_value=input_value)

    with raises(PositiveIntegerEnvironmentVariableError):
        env.get_positive_int(var_name)

    env_reader.get_str.assert_called_once_with(var_name)


@mark.parametrize('input_value, float_value', [('123.28', 123.28), ('-254.74', -254.74), ('123.0', 123), ('1', 1),
                                               ('0.2', 0.2), ('0', 0), ('-0', 0)])
def test_get_float__when_value_is_valid__returns_float(input_value: str, float_value: bool) -> None:
    env_reader.get_str = Mock(return_value=input_value)

    result = env.get_float(var_name)

    env_reader.get_str.assert_called_once_with(var_name)
    assert result == float_value


def test_get_float__when_value_is_invalid__raises_error() -> None:
    env_reader.get_str = Mock(return_value='not float value')

    with raises(FloatEnvironmentVariableError):
        env.get_float(var_name)

    env_reader.get_str.assert_called_once_with(var_name)


@mark.parametrize('input_value, float_value', [('123.28', 123.28), ('254.74', 254.74), ('123.0', 123), ('0.2', 0.2),
                                               ('1', 1)])
def test_get_positive_float__when_value_is_valid__returns_float(input_value: str, float_value: float) -> None:
    env_reader.get_str = Mock(return_value=input_value)

    result = env.get_positive_float(var_name)

    env_reader.get_str.assert_called_once_with(var_name)
    assert result == float_value


@mark.parametrize('input_value', ['-3', '-123.54', '-254.99', '-0.2', '0', '-0'])
def test_get_positive_float__when_value_is_invalid__raises_error(input_value: str) -> None:
    env_reader.get_str = Mock(return_value=input_value)

    with raises(PositiveFloatEnvironmentVariableError):
        env.get_positive_float(var_name)

    env_reader.get_str.assert_called_once_with(var_name)
