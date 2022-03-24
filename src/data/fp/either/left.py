from __future__ import annotations
from typing import (
    Callable,
    Any,
    TypeVar,
)

from .either import Either

L = TypeVar('L')
L2 = TypeVar('L2')
R = Any
R2 = R
T = TypeVar('T')


class _Left(Either[L, R]):
    def __init__(self, value: L) -> None:
        self.__value = value

    @property
    def is_right(self) -> bool:
        return False

    @property
    def is_left(self) -> bool:
        return True

    def map(self, fn: Callable[[R], R2]) -> Either[L, R2]:
        return self

    def map_left(self, fn: Callable[[L], L2]) -> Either[L2, R]:
        return Left(fn(self.__value))

    def bind(self, fn: Callable[[R], Either[L, R2]]) -> Either[L, R2]:
        return self

    def match(self, on_left: Callable[[L], T], on_right: Callable[[R], T]) -> T:
        return on_left(self.__value)

    def get_or(self, value: R) -> R:
        return value

    def get_or_call(self, fn: Callable[[L], R]) -> R:
        return fn(self.__value)

    def get_or_raise(self) -> R:
        if not isinstance(self.__value, Exception):
            raise TypeError(f'{self.__value} is not en exception')
        raise self.__value

    def __repr__(self) -> str:
        return f'Left({repr(self.__value)})'


def Left(value: L) -> Either[L, R]:
    return _Left(value)
