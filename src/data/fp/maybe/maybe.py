from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import (
    Optional,
    Callable,
    Type,
    TypeVar,
    Generic,
)

T = TypeVar('T')
T2 = TypeVar('T2')


class Maybe(Generic[T], metaclass=ABCMeta):
    @staticmethod
    def from_optional(optional: Optional[T]) -> Maybe[T]:
        from .some import Some
        from .nothing import Nothing

        if optional is None:
            return Nothing
        return Some(optional)

    @staticmethod
    def try_except(fn: Callable[[], T], error_type: Type[Exception]) -> Maybe[T]:
        from .some import Some
        from .nothing import Nothing

        try:
            value = fn()
        except Exception as e:
            if not isinstance(e, error_type):
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
    def map(self, fn: Callable[[T], T2]) -> Maybe[T2]: ...

    @abstractmethod
    def bind(self, fn: Callable[[T], Maybe[T2]]) -> Maybe[T2]: ...

    @abstractmethod
    def match(self, on_nothing: Callable[[], T2], on_some: Callable[[T], T2]) -> T2: ...

    @abstractmethod
    def get_or(self, value: T) -> T: ...

    @abstractmethod
    def get_or_call(self, fn: Callable[[], T]) -> T: ...

    @abstractmethod
    def get_or_raise(self) -> T: ...
