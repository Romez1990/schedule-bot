from types import (
    TracebackType,
)
from typing import (
    Awaitable,
    Generator,
    Type,
)

from .manageable_repository_connection import ManageableRepositoryConnection
from .repository_connection import RepositoryConnection


class RepositoryConnectionContextManager:
    def __init__(self, awaitable: Awaitable[ManageableRepositoryConnection]) -> None:
        self.__awaitable = awaitable

    def __await__(self) -> Generator[object, None, RepositoryConnection]:
        return self.__awaitable.__await__()

    __connection: ManageableRepositoryConnection

    async def __aenter__(self) -> RepositoryConnection:
        self.__connection = await self.__awaitable
        return self.__connection

    async def __aexit__(self, exception_type: Type[Exception] | None, exception: Exception | None,
                        exception_traceback: TracebackType | None) -> None:
        self.__connection.release()
