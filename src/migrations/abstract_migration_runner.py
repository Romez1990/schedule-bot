class AbstractMigrationRunner:
    async def run(self) -> None:
        raise NotImplementedError
