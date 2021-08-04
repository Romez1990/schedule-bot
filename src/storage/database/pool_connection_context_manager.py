from types import (
    TracebackType,
)
from typing import (
    Optional,
    Awaitable,
    Generator,
    Type,
)

from .pool_connection import PoolConnection


class PoolConnectionContextManager:
    def __init__(self, awaitable: Awaitable[PoolConnection]) -> None:
        self.__awaitable = awaitable

    def __await__(self) -> Generator[object, None, PoolConnection]:
        return self.__awaitable.__await__()

    __connection: PoolConnection

    async def __aenter__(self) -> PoolConnection:
        self.__connection = await self.__awaitable
        return self.__connection

    async def __aexit__(self, exception_type: Optional[Type[Exception]], exception: Optional[Exception],
                        exception_traceback: Optional[TracebackType]) -> None:
        self.__connection.release()
