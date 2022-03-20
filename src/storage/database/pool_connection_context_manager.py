from types import (
    TracebackType,
)
from typing import (
    Optional,
    Coroutine,
    Generator,
    Type,
)

from .pool_connection import PoolConnection


class PoolConnectionContextManager(Coroutine[object, None, PoolConnection]):
    def __init__(self, coroutine: Coroutine[object, None, PoolConnection]) -> None:
        self.__coroutine = coroutine
        super().__init__()

    def __await__(self) -> Generator[object, None, PoolConnection]:
        return self.__coroutine.__await__()

    def send(self, value: None) -> object:
        res = self.__coroutine.send(value)
        return res

    def throw(self, __typ: Type[BaseException], __val: BaseException | object = ...,
              __tb: Optional[TracebackType] = ...) -> object:
        self.__coroutine.throw(__typ, __val, __tb)

    def close(self) -> None:
        return self.__coroutine.close()

    __connection: PoolConnection

    async def __aenter__(self) -> PoolConnection:
        self.__connection = await self.__coroutine
        return self.__connection

    async def __aexit__(self, exception_type: Optional[Type[Exception]], exception: Optional[Exception],
                        exception_traceback: Optional[TracebackType]) -> None:
        self.__connection.release()
