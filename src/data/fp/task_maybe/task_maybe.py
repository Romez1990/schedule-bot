from __future__ import annotations
from typing import (
    Awaitable,
    Generator,
    Callable,
    Type,
    TypeVar,
    Generic,
    Coroutine,
)

from data.fp.maybe import Maybe, Some, Nothing
from data.fp.task import Task, CoroutineBase, async_identity

T = TypeVar('T')
TResult = TypeVar('TResult')


class TaskMaybe(CoroutineBase[Maybe[T]]):
    def __init__(self, maybe_coroutine: Coroutine[object, None, Maybe[T]]) -> None:
        super().__init__(maybe_coroutine)

    @staticmethod
    def from_maybe(maybe: Maybe[T]) -> TaskMaybe[T]:
        return TaskMaybe(async_identity(maybe))

    @staticmethod
    def try_except(awaitable: Awaitable[T], error_type: Type[Exception]) -> TaskMaybe[T]:
        async def async_try_except() -> Maybe[T]:
            try:
                value = await awaitable
            except Exception as e:
                if not isinstance(e, error_type):
                    raise e
                return Nothing
            return Some(value)

        return TaskMaybe(async_try_except())

    def map(self, fn: Callable[[T], TResult]) -> TaskMaybe[TResult]:
        async def async_map() -> Maybe[T]:
            return (await self._coroutine).map(fn)

        return TaskMaybe(async_map())

    def bind(self, fn: Callable[[T], Maybe[TResult]]) -> TaskMaybe[TResult]:
        async def async_bind() -> Maybe[TResult]:
            maybe = await self._coroutine
            value = maybe if maybe.is_nothing else await maybe.bind(fn)
            return value

        return TaskMaybe(async_bind())

    def match(self, on_nothing: Callable[[], TResult], on_some: Callable[[T], TResult]) -> Task[TResult]:
        async def match() -> TResult:
            return (await self._coroutine).match(on_nothing, on_some)

        return Task(match())

    def match_awaitable(self, on_nothing: Callable[[], Awaitable[TResult]],
                        on_some: Callable[[T], Awaitable[TResult]]) -> Task[TResult]:
        async def match() -> TResult:
            return await (await self._coroutine).match(on_nothing, on_some)

        return Task(match())

    def get_or(self, value: T) -> Task[T]:
        async def async_get_or() -> T:
            return (await self._coroutine).get_or(value)

        return Task(async_get_or())

    def get_or_call(self, fn: Callable[[], T]) -> Task[T]:
        async def async_get_or_call() -> T:
            return (await self._coroutine).get_or_call(fn)

        return Task(async_get_or_call())

    def get_or_raise(self) -> Task[T]:
        async def async_get_or_raise() -> T:
            return (await self._coroutine).get_or_raise()

        return Task(async_get_or_raise())

    def to_maybe(self) -> Task[Maybe[T]]:
        return Task(self._coroutine)
