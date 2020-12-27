from asyncpg import Connection
from returns.maybe import Maybe


class DatabaseState:
    async def connect(self) -> Connection:
        raise NotImplementedError

    async def disconnect(self) -> None:
        raise NotImplementedError

    async def execute(self, query: str, *args: any) -> None:
        raise NotImplementedError

    async def fetch(self, query: str, *args: any) -> list[dict[str, any]]:
        raise NotImplementedError

    async def fetch_row(self, query: str, *args: any) -> Maybe[dict[str, any]]:
        raise NotImplementedError

    async def fetch_value(self, query: str, *args: any) -> any:
        raise NotImplementedError
