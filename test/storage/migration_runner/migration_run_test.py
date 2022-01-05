from pytest import (
    fixture,
    raises,
    mark,
)
from unittest.mock import Mock

from infrastructure.logger import (
    LoggerFactory,
    Logger,
)
from data.fp.task_either import TaskRight, TaskLeft
from storage.database import (
    Database,
    QuerySyntaxError,
    TableAlreadyExistsError,
)
from storage.migration_runner import (
    MigrationRunImpl,
    Migration,
)
from storage.migration_runner.errors import (
    MigrationSyntaxError,
)


@fixture(autouse=True)
def setup() -> None:
    global migration_run, database, logger, migration
    database = Mock()
    logger = Mock()
    logger_factory: LoggerFactory = Mock()
    logger_factory.create = Mock(return_value=logger)
    migration = Mock()
    migration_run = MigrationRunImpl(database, logger_factory, migration)


migration_run: MigrationRunImpl
database: Database
logger: Logger
migration: Migration


@mark.asyncio
async def test__when_database_returns_success__logs_migration_applied() -> None:
    database.execute = Mock(side_effect=[TaskRight(None), TaskRight(None)])
    logger.info = Mock()

    await migration_run.create_table()
    await migration_run.create_relationship()

    assert database.execute.call_count == 2
    logger.log_migration_applied.assert_called_once_with(migration)
    logger_factory.log_migration_failed.assert_not_called()


@mark.asyncio
async def test__when_database_returns_query_syntax_error_for_create_table__raises_migration_syntax_error() -> None:
    database.execute = Mock(return_value=TaskLeft(QuerySyntaxError('')))
    logger_factory.log_migration_applied = Mock()
    logger_factory.log_migration_failed = Mock()

    with raises(MigrationSyntaxError) as e:
        await migration_run.create_table()

    assert 'create_table' in str(e.value)

    assert database.execute.call_count == 1
    logger_factory.log_migration_applied.assert_not_called()
    logger_factory.log_migration_failed.assert_not_called()


@mark.asyncio
async def test__when_database_returns_query_syntax_error_for_create_relationship__raises_migration_syntax_error(
) -> None:
    database.execute = Mock(side_effect=[TaskRight(None), TaskLeft(QuerySyntaxError(''))])
    logger_factory.log_migration_applied = Mock()
    logger_factory.log_migration_failed = Mock()

    await migration_run.create_table()
    with raises(MigrationSyntaxError) as e:
        await migration_run.create_relationship()

    assert 'create_relationship' in str(e.value)

    assert database.execute.call_count == 2
    logger_factory.log_migration_applied.assert_not_called()
    logger_factory.log_migration_failed.assert_not_called()


@mark.asyncio
async def test__when_database_returns_table_exists_error__logs_migration_failed() -> None:
    database.execute = Mock(return_value=TaskLeft(TableAlreadyExistsError('')))
    logger_factory.log_migration_applied = Mock()
    logger_factory.log_migration_failed = Mock()

    await migration_run.create_table()
    await migration_run.create_relationship()

    assert database.execute.call_count == 1
    logger_factory.log_migration_applied.assert_not_called()
    logger_factory.log_migration_failed.assert_called_once()
    assert logger_factory.log_migration_failed.call_args.args[0] == migration
