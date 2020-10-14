class ClassIsNotMigrationError(Exception):
    def __init__(self, migration_name: str) -> None:
        super().__init__(f'class {migration_name} is not a migration')
