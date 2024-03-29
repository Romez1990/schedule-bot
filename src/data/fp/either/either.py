from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    TypeVar,
    Generic,
)

L = TypeVar('L')
LResult = TypeVar('LResult')
R = TypeVar('R')
RResult = TypeVar('RResult')
T = TypeVar('T')


class Either(Generic[L, R], metaclass=ABCMeta):
    @staticmethod
    def try_except(fn: Callable[[], R]) -> Either[Exception, R]:
        from .right import Right
        from .left import Left

        try:
            value = fn()
        except Exception as e:
            return Left(e)
        return Right(value)

    @property
    @abstractmethod
    def is_right(self) -> bool: ...

    @property
    @abstractmethod
    def is_left(self) -> bool: ...

    @abstractmethod
    def map(self, fn: Callable[[R], RResult]) -> Either[L, RResult]: ...

    @abstractmethod
    def map_left(self, fn: Callable[[L], LResult]) -> Either[LResult, R]: ...

    @abstractmethod
    def bind(self, fn: Callable[[R], Either[L, RResult]]) -> Either[L, RResult]: ...

    @abstractmethod
    def match(self, on_left: Callable[[L], T], on_right: Callable[[R], T]) -> T: ...

    @abstractmethod
    def get_or(self, value: R) -> R: ...

    @abstractmethod
    def get_or_call(self, fn: Callable[[L], R]) -> R: ...

    @abstractmethod
    def get_or_raise(self) -> R: ...
