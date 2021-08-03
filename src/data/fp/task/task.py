from __future__ import annotations
from asyncio import (
    gather,
)
from typing import (
    Awaitable,
    Generator,
    Iterable,
    Callable,
    TypeVar,
    Generic,
)

from .async_identity import async_identity

T = TypeVar('T')
T2 = TypeVar('T2')


class Task(Generic[T], Awaitable[T]):
    def __init__(self, value: Awaitable[T]) -> None:
        self.__value = value

    @staticmethod
    def from_value(value: T) -> Task[T]:
        return Task(async_identity(value))

    @staticmethod
    def parallel(tasks: Iterable[Task[T]]) -> Task[list[T]]:
        return Task(gather(*tasks)) \
            .map(list)

    def __await__(self) -> Generator[object, None, T]:
        return self.__value.__await__()

    def map(self, fn: Callable[[T], T2]) -> Task[T2]:
        return Task(self.__async_map(fn))

    def bind(self, fn: Callable[[T], Awaitable[T2]]) -> Task[T2]:
        return Task(self.__async_bind(fn))

    async def __async_map(self, fn: Callable[[T], T2]) -> T2:
        return fn(await self.__value)

    async def __async_bind(self, fn: Callable[[T], Awaitable[T2]]) -> T2:
        return await fn(await self.__value)
