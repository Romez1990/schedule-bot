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
        return TaskMaybe(TaskMaybe.__async_try_except(awaitable, error_type))

    @staticmethod
    async def __async_try_except(awaitable: Awaitable[T], error_type: Type[Exception]) -> Maybe[T]:
        try:
            value = await awaitable
        except Exception as e:
            if not isinstance(e, error_type):
                raise e
            return Nothing
        return Some(value)

    def __await__(self) -> Generator[object, None, Maybe[T]]:
        return self.__value.__await__()

    def map(self, fn: Callable[[T], T2]) -> TaskMaybe[T2]:
        return TaskMaybe(self.__async_map(fn))

    async def __async_map(self, fn: Callable[[T], T2]) -> Maybe[T]:
        return (await self.__value).map(fn)

    def bind(self, fn: Callable[[T], Maybe[T2]]) -> TaskMaybe[T2]:
        return TaskMaybe(self.__async_bind(fn))

    async def __async_bind(self, fn: Callable[[T], Maybe[T2]]) -> Maybe[T2]:
        maybe = await self.__value
        value = maybe if maybe.is_nothing else await maybe.bind(fn)
        return value

    def get_or(self, value: T) -> Task[T]:
        return Task(self.__async_get_or(value))

    async def __async_get_or(self, value: T) -> T:
        return (await self.__value).get_or(value)

    def get_or_call(self, fn: Callable[[], T]) -> Task[T]:
        return Task(self.__async_get_or_call(fn))

    async def __async_get_or_call(self, fn: Callable[[], T]) -> T:
        return (await self.__value).get_or_call(fn)

    def get_or_raise(self) -> Task[T]:
        return Task(self.__async_get_or_raise())

    async def __async_get_or_raise(self) -> T:
        return (await self.__value).get_or_raise()

    def to_maybe(self) -> Task[Maybe[T]]:
        return Task(self.__value)
