from types import (
    TracebackType,
)
from typing import (
    Coroutine,
    Type,
)

from data.fp.task import CoroutineBase
from .manageable_repository_connection import ManageableRepositoryConnection
from .repository_connection import RepositoryConnection


class RepositoryConnectionContextManager(CoroutineBase[ManageableRepositoryConnection]):
    def __init__(self, connection_coroutine: Coroutine[object, None, ManageableRepositoryConnection]) -> None:
        super().__init__(connection_coroutine)

    __connection: ManageableRepositoryConnection

    async def __aenter__(self) -> RepositoryConnection:
        self.__connection = await self._coroutine
        return self.__connection

    async def __aexit__(self, exception_type: Type[Exception] | None, exception: Exception | None,
                        exception_traceback: TracebackType | None) -> None:
        self.__connection.release()
