from __future__ import annotations
from collections.abc import Coroutine
from types import (
    TracebackType,
)
from typing import (
    Generator,
    Type,
    TypeVar,
    Generic,
    Awaitable,
    Coroutine,
    cast,
)

T = TypeVar('T')


class CoroutineBase(Coroutine[object, None, T], Generic[T]):
    def __init__(self, awaitable: Awaitable[T]) -> None:
        self._coroutine = awaitable if isinstance(awaitable, Coroutine) else self.__to_coroutine(awaitable)

    async def __to_coroutine(self, awaitable: Awaitable[T]) -> T:
        return await awaitable

    def __await__(self) -> Generator[object, None, T]:
        return self._coroutine.__await__()

    def send(self, value: None) -> object:
        return self._coroutine.send(value)

    def throw(self, exception_type: BaseException | Type[BaseException], value: object | None = None,
              traceback: TracebackType = None) -> object:
        return self._coroutine.throw(cast(Type[BaseException], exception_type), value, traceback)

    def close(self) -> None:
        self._coroutine.close()
