from asyncio import (
    create_task,
)
from pytest import (
    fixture,
    raises,
    mark,
)
from unittest.mock import Mock

from storage.database import (
    ConnectionPoolImpl,
    ConnectionFactory,
    Connection,
    GetConnectionTimeoutError,
)
from infrastructure.config import Config
from data.fp.task import Task


@fixture(autouse=True)
def setup() -> None:
    global connection_pool, connection_factory
    connection_factory = Mock()
    config: Config = Mock()
    config.db_connection_pool_size = 2
    config.db_connection_release_timeout = 0.001
    connection_pool = ConnectionPoolImpl(connection_factory, config)


connection_pool: ConnectionPoolImpl
connection_factory: ConnectionFactory


@mark.asyncio
async def test_init__calls_factory_create_connection() -> None:
    connection: Connection = Mock()
    connection.open = Mock(return_value=Task.from_value(None))
    connection_factory.create = Mock(return_value=connection)

    await connection_pool.init()

    connection_factory.create.assert_called_once_with()


@mark.asyncio
async def test_get_connection__calls_factory_create_connection() -> None:
    connection: Connection = Mock()
    connection.open = Mock(return_value=Task.from_value(None))
    connection_factory.create = Mock(return_value=connection)

    result_connection = await connection_pool.get_connection()

    assert result_connection is connection
    connection_factory.create.assert_called_once_with()


@mark.asyncio
async def test_get_connection__when_call_2_times__returns_different_connections() -> None:
    connection_1: Connection = Mock()
    connection_1.open = Mock(return_value=Task.from_value(None))
    connection_2: Connection = Mock()
    connection_2.open = Mock(return_value=Task.from_value(None))
    connection_factory.create = Mock(side_effect=[connection_1, connection_2])

    result_connection_1 = await connection_pool.get_connection()
    result_connection_2 = await connection_pool.get_connection()

    assert result_connection_1 is connection_1
    assert result_connection_2 is connection_2
    assert connection_factory.create.call_count == 2


@mark.asyncio
async def test_release_connection__when_get_connection__returns_the_same_connection() -> None:
    connection: Connection = Mock()
    connection.open = Mock(return_value=Task.from_value(None))
    connection_factory.create = Mock(return_value=connection)

    result_connection = await connection_pool.get_connection()
    connection_pool.release_connection(result_connection)
    result_connection_2 = await connection_pool.get_connection()

    assert result_connection_2 is connection
    connection_factory.create.assert_called_once_with()


@mark.asyncio
async def test_get_connection__when_get_connection__waits_for_release() -> None:
    connection_1: Connection = Mock()
    connection_1.open = Mock(return_value=Task.from_value(None))
    connection_2: Connection = Mock()
    connection_2.open = Mock(return_value=Task.from_value(None))
    connection_factory.create = Mock(side_effect=[connection_1, connection_2])

    result_connection_1 = await connection_pool.get_connection()
    await connection_pool.get_connection()  # result_connection_2
    result_connection_3_task = create_task(connection_pool.get_connection())
    connection_pool.release_connection(result_connection_1)

    assert await result_connection_3_task is result_connection_1
    assert connection_factory.create.call_count == 2


@mark.asyncio
async def test_get_connection__when_get_connection__no_return() -> None:
    connection_1: Connection = Mock()
    connection_1.open = Mock(return_value=Task.from_value(None))
    connection_2: Connection = Mock()
    connection_2.open = Mock(return_value=Task.from_value(None))
    connection_factory.create = Mock(side_effect=[connection_1, connection_2])

    await connection_pool.get_connection()  # result_connection_1
    await connection_pool.get_connection()  # result_connection_2
    with raises(GetConnectionTimeoutError):
        await connection_pool.get_connection()
