from infrastructure.logger import LoggerFactory
from data.fp.either import Either
from data.fp.task import Task
from data.fp.task_either import TaskEither
from storage.database import (
    Database,
    DatabaseError,
    QuerySyntaxError,
    TableAlreadyExistsError,
)
from .errors import (
    MigrationTableAlreadyExistsError,
    MigrationSyntaxError,
)
from .migration_run import MigrationRun
from .migration import Migration


class MigrationRunImpl(MigrationRun):
    def __init__(self, database: Database, logger_factory: LoggerFactory, migration: Migration) -> None:
        self.__database = database
        self.__logger = logger_factory.create()
        self.__migration = migration

    __create_table_result: Either[MigrationTableAlreadyExistsError, None]

    def create_table(self) -> Task[None]:
        query_name = 'create_table'

        def filter_error(error: DatabaseError) -> MigrationTableAlreadyExistsError:
            if isinstance(error, QuerySyntaxError):
                raise MigrationSyntaxError(self.__migration, query_name) from error
            if isinstance(error, TableAlreadyExistsError):
                return MigrationTableAlreadyExistsError(self.__migration)
            raise error

        def set_result(result: Either[MigrationTableAlreadyExistsError, None]) -> None:
            self.__create_table_result = result

        query = getattr(self.__migration, query_name)
        return self.__database.execute(query) \
            .map_left(filter_error) \
            .to_task() \
            .map(set_result)

    def create_relationship(self) -> Task[None]:
        return TaskEither.from_either(self.__create_table_result) \
            .bind_task(self.__create_relationships) \
            .match(self.__log_migration_failure, self.__log_migration_success)

    def __create_relationships(self, _: None) -> Task[None]:
        query_name = 'create_relationships'

        if not hasattr(self.__migration, query_name):
            return Task.from_value(None)

        def filter_error(error: DatabaseError) -> DatabaseError:
            if isinstance(error, QuerySyntaxError):
                raise MigrationSyntaxError(self.__migration, query_name) from error
            return error

        query = getattr(self.__migration.create_relationships, query_name)
        return self.__database.execute(query) \
            .map_left(filter_error) \
            .get_or_raise()

    def __log_migration_success(self, _: None) -> None:
        migration_name = type(self.__migration).__name__
        self.__logger.info(f'Migration {migration_name} applied')

    def __log_migration_failure(self, error: MigrationTableAlreadyExistsError) -> None:
        self.__logger.info(str(error))
