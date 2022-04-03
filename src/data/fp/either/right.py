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


class _Right(Either[L, R]):
    def __init__(self, value: R) -> None:
        self.__value = value

    @property
    def is_right(self) -> bool:
        return True

    @property
    def is_left(self) -> bool:
        return False

    def map(self, fn: Callable[[R], RResult]) -> Either[L, RResult]:
        return Right(fn(self.__value))

    def map_left(self, fn: Callable[[L], LResult]) -> Either[LResult, R]:
        return cast(Either[LResult, R], self)

    def bind(self, fn: Callable[[R], Either[L, RResult]]) -> Either[L, RResult]:
        return fn(self.__value)

    def match(self, on_left: Callable[[L], TResult], on_right: Callable[[R], TResult]) -> TResult:
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
