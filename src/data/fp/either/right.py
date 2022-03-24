from __future__ import annotations
from typing import (
    Callable,
    TypeVar,
    cast,
)

from .either import Either

L = TypeVar('L')
L2 = TypeVar('L2')
R = TypeVar('R')
R2 = TypeVar('R2')
T = TypeVar('T')


class _Right(Either[L, R]):
    def __init__(self, value: R) -> None:
        self.__value = value

    @property
    def is_right(self) -> bool:
        return True

    @property
    def is_left(self) -> bool:
        return False

    def map(self, fn: Callable[[R], R2]) -> Either[L, R2]:
        return Right(fn(self.__value))

    def map_left(self, fn: Callable[[L], L2]) -> Either[L2, R]:
        return cast(Either[L2, R], self)

    def bind(self, fn: Callable[[R], Either[L, R2]]) -> Either[L, R2]:
        return fn(self.__value)

    def match(self, on_left: Callable[[L], T], on_right: Callable[[R], T]) -> T:
        return on_right(self.__value)

    def get_or(self, value: R) -> R:
        return self.__value

    def get_or_call(self, fn: Callable[[L], R]) -> R:
        return self.__value

    def get_or_raise(self) -> R:
        return self.__value

    def __repr__(self) -> str:
        return f'Right({repr(self.__value)})'


def Right(value: R) -> Either[L, R]:
    return _Right(value)
