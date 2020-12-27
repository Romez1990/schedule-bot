from .migration import Migration


class MigrationRepositoryInterface:
    def get_all(self) -> list[Migration]:
        raise NotImplementedError
