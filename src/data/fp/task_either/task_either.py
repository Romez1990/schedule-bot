from __future__ import annotations
from typing import (
    Awaitable,
    Generator,
    Callable,
    TypeVar,
    Generic,
)

from data.fp.either import Either, Right, Left
from data.fp.task import Task, async_identity

L = TypeVar('L')
L2 = TypeVar('L2')
R = TypeVar('R')
R2 = TypeVar('R2')
T = TypeVar('T')


class TaskEither(Generic[L, R], Awaitable[Either[L, R]]):
    def __init__(self, awaitable_either: Awaitable[Either[L, R]]) -> None:
        self.__value = awaitable_either

    @staticmethod
    def from_either(either: Either[L, R]) -> TaskEither[L, R]:
        return TaskEither(async_identity(either))

    @staticmethod
    def try_except(awaitable: Awaitable[R]) -> TaskEither[Exception, R]:
        return TaskEither(TaskEither.__async_try_except(awaitable))

    @staticmethod
    async def __async_try_except(awaitable: Awaitable[R]) -> Either[Exception, R]:
        try:
            value = await awaitable
        except Exception as e:
            return Left(e)
        return Right(value)

    def __await__(self) -> Generator[object, None, Either[L, R]]:
        return self.__value.__await__()

    def map(self, fn: Callable[[R], R2]) -> TaskEither[L, R2]:
        return TaskEither(self.__async_map(fn))

    async def __async_map(self, fn: Callable[[R], R2]) -> Either[L, 2]:
        return (await self.__value).map(fn)

    def map_left(self, fn: Callable[[L], L2]) -> TaskEither[L2, R]:
        return TaskEither(self.__async_map_left(fn))

    async def __async_map_left(self, fn: Callable[[L], L2]) -> Either[L2, R]:
        return (await self.__value).map_left(fn)

    def map_task(self, fn: Callable[[Either[L, R]], Either[L2, R2]]) -> TaskEither[L2, R2]:
        return TaskEither(self.__async_map_task(fn))

    async def __async_map_task(self, fn: Callable[[Either[L, R]], Either[L2, R2]]) -> Either[L2, R2]:
        return fn(await self.__value)

    def bind(self, fn: Callable[[R], TaskEither[L, R2]]) -> TaskEither[L, R2]:
        return TaskEither(self.__async_bind(fn))

    async def __async_bind(self, fn: Callable[[R], TaskEither[L, R2]]) -> Either[L, R2]:
        either = await self.__value
        return either if either.is_left else await either.bind(fn)

    def bind_awaitable(self, fn: Callable[[R], Awaitable[R2]]) -> TaskEither[L, R2]:
        return TaskEither(self.__async_awaitable_task(fn))

    async def __async_awaitable_task(self, fn: Callable[[R], Awaitable[R2]]) -> Either[L, R2]:
        either = await self.__value
        return either if either.is_left else Right(await either.bind(fn))

    def get_or(self, value: R) -> Task[R]:
        return Task(self.__async_get_or(value))

    async def __async_get_or(self, value: R) -> R:
        return (await self.__value).get_or(value)

    def get_or_call(self, fn: Callable[[L], R]) -> Task[R]:
        return Task(self.__async_get_or_call(fn))

    async def __async_get_or_call(self, fn: Callable[[L], R]) -> R:
        return (await self.__value).get_or_call(fn)

    def get_or_raise(self) -> Task[R]:
        return Task(self.__async_get_or_raise())

    async def __async_get_or_raise(self) -> R:
        return (await self.__value).get_or_raise()

    def to_task(self) -> Task[Either[L, R]]:
        return Task(self.__value)

    def match(self, on_left: Callable[[L], T], on_right: Callable[[R], T]) -> Task[T]:
        return Task(self.__async_match(on_left, on_right))

    async def __async_match(self, on_left: Callable[[L], T], on_right: Callable[[R], T]) -> T:
        return (await self.__value).match(on_left, on_right)
