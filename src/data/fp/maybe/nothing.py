from __future__ import annotations
from typing import (
    Callable,
    Any,
    TypeVar,
)

from .maybe import Maybe
from .nothing_error import NothingError

T = Any
T2 = TypeVar('T2')


class _Nothing(Maybe[T]):
    @property
    def is_some(self) -> bool:
        return False

    @property
    def is_nothing(self) -> bool:
        return True

    def map(self, fn: Callable[[T], T2]) -> Maybe[T2]:
        return self

    def bind(self, fn: Callable[[T], Maybe[T2]]) -> Maybe[T2]:
        return self

    def match(self, on_nothing: Callable[[], T2], on_some: Callable[[T], T2]) -> T2:
        return on_nothing()

    def get_or(self, value: T) -> T:
        return value

    def get_or_call(self, fn: Callable[[], T]) -> T:
        return fn()

    def get_or_raise(self) -> T:
        raise NothingError()

    def __str__(self) -> str:
        return '<Nothing>'


Nothing = _Nothing()
