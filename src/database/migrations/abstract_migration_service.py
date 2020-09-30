class AbstractMigrationService:
    async def run(self) -> None:
        raise NotImplementedError
