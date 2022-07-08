from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import (
    Callable,
    Type,
    TypeVar,
    Generic,
)

T = TypeVar('T')
TResult = TypeVar('TResult')


class Maybe(Generic[T], metaclass=ABCMeta):
    @staticmethod
    def from_optional(optional: T | None) -> Maybe[T]:
        from .some import Some
        from .nothing import Nothing

        if optional is None:
            return Nothing
        return Some(optional)

    @staticmethod
    def try_except(fn: Callable[[], T], error_class: Type[Exception]) -> Maybe[T]:
        from .some import Some
        from .nothing import Nothing

        try:
            value = fn()
        except Exception as e:
            if not isinstance(e, error_class):
                raise e
            return Nothing
        return Some(value)

    @property
    @abstractmethod
    def is_some(self) -> bool: ...

    @property
    @abstractmethod
    def is_nothing(self) -> bool: ...

    @abstractmethod
    def map(self, fn: Callable[[T], TResult]) -> Maybe[TResult]: ...

    @abstractmethod
    def bind(self, fn: Callable[[T], Maybe[TResult]]) -> Maybe[TResult]: ...

    @abstractmethod
    def match(self, on_nothing: Callable[[], TResult], on_some: Callable[[T], TResult]) -> TResult: ...

    @abstractmethod
    def get_or(self, value: T) -> T: ...

    @abstractmethod
    def get_or_none(self) -> T | None: ...

    @abstractmethod
    def get_or_call(self, fn: Callable[[], T]) -> T: ...

    @abstractmethod
    def get_or_raise(self) -> T: ...

    @abstractmethod
    def __eq__(self, other: object) -> bool: ...
