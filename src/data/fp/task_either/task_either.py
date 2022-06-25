from __future__ import annotations
from typing import (
    Awaitable,
    Coroutine,
    Callable,
    TypeVar,
)

from data.fp.either import Either, Right, Left
from data.fp.task import Task, CoroutineBase, async_identity

L = TypeVar('L')
LResult = TypeVar('LResult')
R = TypeVar('R')
RResult = TypeVar('RResult')
TResult = TypeVar('TResult')


class TaskEither(CoroutineBase[Either[L, R]]):
    def __init__(self, either_coroutine: Coroutine[object, None, Either[L, R]]) -> None:
        super().__init__(either_coroutine)

    @staticmethod
    def from_either(either: Either[L, R]) -> TaskEither[L, R]:
        return TaskEither(async_identity(either))

    @staticmethod
    def try_except(awaitable: Awaitable[R]) -> TaskEither[Exception, R]:
        async def async_try_except() -> Either[Exception, R]:
            try:
                value = await awaitable
            except Exception as e:
                return Left(e)
            return Right(value)

        return TaskEither(async_try_except())

    def map(self, fn: Callable[[R], RResult]) -> TaskEither[L, RResult]:
        async def async_map() -> Either[L, 2]:
            return (await self._coroutine).map(fn)

        return TaskEither(async_map())

    def map_left(self, fn: Callable[[L], LResult]) -> TaskEither[LResult, R]:
        async def async_map_left() -> Either[LResult, R]:
            return (await self._coroutine).map_left(fn)

        return TaskEither(async_map_left())

    def map_task(self, fn: Callable[[Either[L, R]], Either[LResult, RResult]]) -> TaskEither[LResult, RResult]:
        async def async_map_task() -> Either[LResult, RResult]:
            return fn(await self._coroutine)

        return TaskEither(async_map_task())

    def bind(self, fn: Callable[[R], TaskEither[L, RResult]]) -> TaskEither[L, RResult]:
        async def async_bind() -> Either[L, RResult]:
            either = await self._coroutine
            return either if either.is_left else await either.bind(fn)

        return TaskEither(async_bind())

    def bind_awaitable(self, fn: Callable[[R], Awaitable[RResult]]) -> TaskEither[L, RResult]:
        async def async_awaitable_task() -> Either[L, RResult]:
            either = await self._coroutine
            return either if either.is_left else Right(await either.bind(fn))

        return TaskEither(async_awaitable_task())

    def get_or(self, value: R) -> Task[R]:
        async def async_get_or() -> R:
            return (await self._coroutine).get_or(value)

        return Task(async_get_or())

    def get_or_call(self, fn: Callable[[L], R]) -> Task[R]:
        async def async_get_or_call() -> R:
            return (await self._coroutine).get_or_call(fn)

        return Task(async_get_or_call())

    def get_or_raise(self) -> Task[R]:
        async def async_get_or_raise() -> R:
            return (await self._coroutine).get_or_raise()

        return Task(async_get_or_raise())

    def to_task(self) -> Task[Either[L, R]]:
        return Task(self._coroutine)

    def match(self, on_left: Callable[[L], TResult], on_right: Callable[[R], TResult]) -> Task[TResult]:
        async def async_match() -> TResult:
            return (await self._coroutine).match(on_left, on_right)

        return Task(async_match())

