class MigrationServiceInterface:
    async def run(self) -> None:
        raise NotImplementedError
