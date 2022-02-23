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
    cast,
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
    def parallel(tasks: Iterable[Awaitable[T]]) -> Task[list[T]]:
        return Task(cast(Awaitable[list[T]], gather(*tasks)))

    def __await__(self) -> Generator[object, None, T]:
        return self.__value.__await__()

    def map(self, fn: Callable[[T], T2]) -> Task[T2]:
        async def async_map() -> T2:
            return fn(await self.__value)

        return Task(async_map())

    def bind(self, fn: Callable[[T], Awaitable[T2]]) -> Task[T2]:
        async def async_bind() -> T2:
            return await fn(await self.__value)

        return Task(async_bind())
