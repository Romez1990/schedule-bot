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

from data.vector import List
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
        def reducer(results_task: Task[list[T]], task: Task[T]) -> Task[list[T]]:
            def binder(results: list[T]) -> Task[list[T]]:
                def mapper(value: T) -> list[T]:
                    results.append(value)
                    return results

                return task.map(mapper)

            return results_task.bind(binder)

        return List(tasks) \
            .reduce(reducer, Task.from_value([]))

    def map(self, fn: Callable[[T], T2]) -> Task[T2]:
        async def async_map() -> T2:
            return fn(await self._coroutine)

        return Task(async_map())

    def bind(self, fn: Callable[[T], Awaitable[T2]]) -> Task[T2]:
        async def async_bind() -> T2:
            return await fn(await self._coroutine)

        return Task(async_bind())
