from types import (
    TracebackType,
)
from typing import (
    Optional,
    Coroutine,
    Type,
)

from data.fp.task import CoroutineBase
from .pool_connection import PoolConnection


class PoolConnectionContextManager(CoroutineBase[PoolConnection]):
    def __init__(self, coroutine: Coroutine[object, None, PoolConnection]) -> None:
        super().__init__(coroutine)

    __connection: PoolConnection

    async def __aenter__(self) -> PoolConnection:
        self.__connection = await self._coroutine
        return self.__connection

    async def __aexit__(self, exception_type: Optional[Type[Exception]], exception: Optional[Exception],
                        exception_traceback: Optional[TracebackType]) -> None:
        self.__connection.release()
