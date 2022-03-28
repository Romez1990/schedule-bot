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
    cast,
)

T = TypeVar('T')


class CoroutineBase(Coroutine[object, None, T], Generic[T]):
    def __init__(self, coroutine: Coroutine[object, None, T]) -> None:
        self._coroutine = coroutine

    def __await__(self) -> Generator[object, None, T]:
        return self._coroutine.__await__()

    def send(self, value: None) -> object:
        return self._coroutine.send(value)

    def throw(self, exception_type: BaseException | Type[BaseException], value: object | None = None,
              traceback: TracebackType = None) -> object:
        return self._coroutine.throw(cast(Type[BaseException], exception_type), value, traceback)

    def close(self) -> None:
        self._coroutine.close()
