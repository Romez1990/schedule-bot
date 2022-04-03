from __future__ import annotations
from typing import (
    Callable,
    TypeVar,
    cast,
)

from .either import Either

L = TypeVar('L')
LResult = TypeVar('LResult')
R = TypeVar('R')
RResult = TypeVar('RResult')
TResult = TypeVar('TResult')


class _Left(Either[L, R]):
    def __init__(self, value: L) -> None:
        self.__value = value

    @property
    def is_right(self) -> bool:
        return False

    @property
    def is_left(self) -> bool:
        return True

    def map(self, fn: Callable[[R], RResult]) -> Either[L, RResult]:
        return cast(Either[L, RResult], self)

    def map_left(self, fn: Callable[[L], LResult]) -> Either[LResult, R]:
        return Left(fn(self.__value))

    def bind(self, fn: Callable[[R], Either[L, RResult]]) -> Either[L, RResult]:
        return cast(Either[L, RResult], self)

    def match(self, on_left: Callable[[L], TResult], on_right: Callable[[R], TResult]) -> TResult:
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
