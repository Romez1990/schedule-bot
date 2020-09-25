class AbstractTelegramDispatcher:
    async def start(self) -> None:
        raise NotImplementedError
