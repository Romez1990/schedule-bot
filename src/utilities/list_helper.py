from typing import (
    TypeVar,
    Iterable,
    Callable,
)

from returns.maybe import Maybe, Some, Nothing

T = TypeVar('T')
R = TypeVar('R')


class ListHelper:
    def find_first(self, collection: Iterable[T], predicate: Callable[[T], bool]) -> Maybe[T]:
        for element in collection:
            if predicate(element):
                return Some(element)
        return Nothing

    def find_first_map(self, collection: Iterable[T], func: Callable[[T], Maybe[R]]) -> Maybe[R]:
        for element in collection:
            result = func(element)
            if result != Nothing:
                return result
        return Nothing
