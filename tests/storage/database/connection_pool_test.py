from __future__ import annotations

from asyncio import (
    create_task,
)
from typing import (
    Callable,
)
from pytest import (
    fixture,
    raises,
    mark,
)
from unittest.mock import Mock

from storage.database import (
    ConnectionPoolImpl,
    PoolConnectionFactory,
    ManageablePoolConnection,
    PoolConnectionImpl,
    GetConnectionTimeoutError,
)
from infrastructure.config import Config
from data.fp.task import Task


@fixture(autouse=True)
def setup() -> None:
    global connection_pool, connection_factory
    connection_factory = Mock()
    config: Config = Mock()
    config.db_connection_pool_max_size = 2
    config.db_connection_pool_timeout = 0.001
    connection_pool = ConnectionPoolImpl(connection_factory, config)


def mock_connection_factory_create() -> Mock:
    def create_connection(on_released: Callable[[], None]) -> ManageablePoolConnection:
        connection: ManageablePoolConnection = Mock()
        connection.open = Mock(return_value=Task.from_value(None))
        return PoolConnectionImpl(connection, on_released)

    return Mock(side_effect=create_connection)


connection_pool: ConnectionPoolImpl
connection_factory: PoolConnectionFactory


@mark.asyncio
async def test_init__calls_factory_create_connection() -> None:
    connection_factory.create = mock_connection_factory_create()

    await connection_pool.init()

    connection_factory.create.assert_called_once()


@mark.asyncio
async def test_get_connection__calls_factory_create_connection() -> None:
    connection_factory.create = mock_connection_factory_create()

    result_connection = await connection_pool.get_connection()

    connection_factory.create.assert_called_once()
    result_connection.release()


@mark.asyncio
async def test_get_connection__when_call_2_times__returns_different_connections() -> None:
    connection_factory.create = mock_connection_factory_create()

    result_connection_1 = await connection_pool.get_connection()
    result_connection_2 = await connection_pool.get_connection()

    assert result_connection_1 is not result_connection_2
    assert connection_factory.create.call_count == 2
    result_connection_1.release()
    result_connection_2.release()


@mark.asyncio
async def test_release_connection__when_get_connection__returns_the_same_connection() -> None:
    connection_factory.create = mock_connection_factory_create()

    result_connection = await connection_pool.get_connection()
    result_connection.release()
    result_connection_2 = await connection_pool.get_connection()

    assert result_connection_2 is result_connection
    connection_factory.create.assert_called_once()
    result_connection_2.release()


@mark.asyncio
async def test_get_connection__when_get_connection__waits_for_release() -> None:
    connection_factory.create = mock_connection_factory_create()

    result_connection_1 = await connection_pool.get_connection()
    result_connection_2 = await connection_pool.get_connection()
    result_connection_3_task = create_task(connection_pool.get_connection())
    result_connection_1.release()
    result_connection_3 = await result_connection_3_task

    assert result_connection_3 is result_connection_1
    assert result_connection_2 is not result_connection_1
    assert connection_factory.create.call_count == 2
    result_connection_2.release()
    result_connection_3.release()


@mark.asyncio
async def test_get_connection__when_get_connection__no_return() -> None:
    connection_factory.create = mock_connection_factory_create()

    # noinspection PyUnusedLocal
    result_connection_1 = await connection_pool.get_connection()
    # noinspection PyUnusedLocal
    result_connection_2 = await connection_pool.get_connection()
    with raises(GetConnectionTimeoutError):
        await connection_pool.get_connection()

    result_connection_1.release()
    result_connection_2.release()
