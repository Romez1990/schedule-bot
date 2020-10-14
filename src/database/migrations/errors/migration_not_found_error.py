class MigrationNotFoundError(Exception):
    def __init__(self, module_name: str) -> None:
        super().__init__(f'module {module_name} does not contain migration')
