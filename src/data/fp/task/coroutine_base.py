from __future__ import annotations
from collections.abc import Coroutine
from types import (
    TracebackType,
)
from typing import (
    Optional,
    Generator,
    Type,
    TypeVar,
    Generic,
)

T = TypeVar('T')


class CoroutineBase(Coroutine[object, None, T], Generic[T]):
    def __init__(self, coroutine: Coroutine[object, None, T]) -> None:
        self._coroutine = coroutine

    def __await__(self) -> Generator[object, None, T]:
        return self._coroutine.__await__()

    def send(self, value: None) -> object:
        return self._coroutine.send(value)

    def throw(self, exception_type: Type[BaseException], value: BaseException | object = ...,
              traceback: Optional[TracebackType] = None) -> object:
        return self._coroutine.throw(exception_type, value, traceback)

    def close(self) -> None:
        self._coroutine.close()
