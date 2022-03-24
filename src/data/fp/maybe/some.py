from __future__ import annotations
from typing import (
    Callable,
    TypeVar,
)

from .maybe import Maybe

T = TypeVar('T')
T2 = TypeVar('T2')


class Some(Maybe[T]):
    def __init__(self, value: T) -> None:
        self.__value = value

    @property
    def is_some(self) -> bool:
        return True

    @property
    def is_nothing(self) -> bool:
        return False

    def map(self, fn: Callable[[T], T2]) -> Maybe[T2]:
        return Some(fn(self.__value))

    def bind(self, fn: Callable[[T], Maybe[T2]]) -> Maybe[T2]:
        return fn(self.__value)

    def match(self, on_nothing: Callable[[], T2], on_some: Callable[[T], T2]) -> T2:
        return on_some(self.__value)

    def get_or(self, value: T) -> T:
        return self.__value

    def get_or_call(self, fn: Callable[[], T]) -> T:
        return self.__value

    def get_or_raise(self) -> T:
        return self.__value

    def __repr__(self) -> str:
        return f'Some({repr(self.__value)})'
