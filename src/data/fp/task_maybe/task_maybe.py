from __future__ import annotations
from typing import (
    Awaitable,
    Generator,
    Callable,
    Type,
    TypeVar,
    Generic,
)

from data.fp.maybe import Maybe, Some, Nothing
from data.fp.task import Task, async_identity

T = TypeVar('T')
T2 = TypeVar('T2')


class TaskMaybe(Generic[T], Awaitable[Maybe[T]]):
    def __init__(self, awaitable_maybe: Awaitable[Maybe[T]]) -> None:
        self.__value = awaitable_maybe

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

    def __await__(self) -> Generator[object, None, Maybe[T]]:
        return self.__value.__await__()

    def map(self, fn: Callable[[T], T2]) -> TaskMaybe[T2]:
        async def async_map() -> Maybe[T]:
            return (await self.__value).map(fn)

        return TaskMaybe(async_map())

    def bind(self, fn: Callable[[T], Maybe[T2]]) -> TaskMaybe[T2]:
        async def async_bind() -> Maybe[T2]:
            maybe = await self.__value
            value = maybe if maybe.is_nothing else await maybe.bind(fn)
            return value

        return TaskMaybe(async_bind())

    def match(self, on_nothing: Callable[[], T2], on_some: Callable[[T], T2]) -> Task[T2]:
        async def match() -> T2:
            return (await self.__value).match(on_nothing, on_some)

        return Task(match())

    def match_awaitable(self, on_nothing: Callable[[], Awaitable[T2]],
                        on_some: Callable[[T], Awaitable[T2]]) -> Task[T2]:
        async def match() -> T2:
            return await (await self.__value).match(on_nothing, on_some)

        return Task(match())

    def get_or(self, value: T) -> Task[T]:
        async def async_get_or() -> T:
            return (await self.__value).get_or(value)

        return Task(async_get_or())

    def get_or_call(self, fn: Callable[[], T]) -> Task[T]:
        async def async_get_or_call() -> T:
            return (await self.__value).get_or_call(fn)

        return Task(async_get_or_call())

    def get_or_raise(self) -> Task[T]:
        async def async_get_or_raise() -> T:
            return (await self.__value).get_or_raise()

        return Task(async_get_or_raise())

    def to_maybe(self) -> Task[Maybe[T]]:
        return Task(self.__value)
