from __future__ import annotations
from typing import (
    Callable,
    Any,
    TypeVar,
)

from .maybe import Maybe
from .nothing_error import NothingError

T = Any
TResult = TypeVar('TResult')


class _Nothing(Maybe[T]):
    @property
    def is_some(self) -> bool:
        return False

    @property
    def is_nothing(self) -> bool:
        return True

    def map(self, fn: Callable[[T], TResult]) -> Maybe[TResult]:
        return self

    def bind(self, fn: Callable[[T], Maybe[TResult]]) -> Maybe[TResult]:
        return self

    def match(self, on_nothing: Callable[[], TResult], on_some: Callable[[T], TResult]) -> TResult:
        return on_nothing()

    def get_or(self, value: T) -> T:
        return value

    def get_or_none(self) -> T | None:
        return None

    def get_or_call(self, fn: Callable[[], T]) -> T:
        return fn()

    def get_or_raise(self) -> T:
        raise NothingError()

    def __eq__(self, other: object) -> bool:
        return isinstance(other, _Nothing)

    def __repr__(self) -> str:
        return 'Nothing'


Nothing = _Nothing()
