from __future__ import annotations
from asyncio import (
    gather,
)
from typing import (
    Awaitable,
    Coroutine,
    Iterable,
    Callable,
    TypeVar,
    Generic,
    cast,
)

from .coroutine_base import CoroutineBase
from .async_identity import async_identity

T = TypeVar('T')
T2 = TypeVar('T2')


class Task(CoroutineBase[T], Generic[T]):
    def __init__(self, coroutine: Coroutine[object, None, T]) -> None:
        super().__init__(coroutine)

    @staticmethod
    def from_value(value: T) -> Task[T]:
        return Task(async_identity(value))

    @staticmethod
    def parallel(tasks: Iterable[Awaitable[T]]) -> Task[list[T]]:
        return Task(cast(Coroutine[object, None, list[T]], gather(*tasks)))

    @staticmethod
    def series(tasks: Iterable[Task[T]]) -> Task[list[T]]:
        async def async_series() -> list[T]:
            results = []
            for task in tasks:
                value = await task
                results.append(value)
            return results

        return Task(async_series())

    def map(self, fn: Callable[[T], T2]) -> Task[T2]:
        async def async_map() -> T2:
            return fn(await self._coroutine)

        return Task(async_map())

    def bind(self, fn: Callable[[T], Awaitable[T2]]) -> Task[T2]:
        async def async_bind() -> T2:
            return await fn(await self._coroutine)

        return Task(async_bind())
