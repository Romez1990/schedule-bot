from __future__ import annotations
from functools import reduce
from collections.abc import Sequence
from typing import (
    Optional,
    Callable,
    Iterable,
    Type,
    TypeVar,
    overload,
)

from data.fp.either import Either, Right, Left
from data.fp.maybe import Maybe, Nothing
from data.fp.type import cast

T = TypeVar('T')
T2 = TypeVar('T2')


class List(Sequence[T]):
    def __init__(self, iterable: Iterable[T] = None) -> None:
        self.__data = self.__create_list(iterable)

    def __create_list(self, iterable: Optional[Iterable[T]]) -> tuple[T, ...]:
        if iterable is None:
            return tuple()
        if isinstance(iterable, List):
            return iterable.__data
        return tuple(iterable)

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, slice_: slice) -> Sequence[T]: ...

    def __getitem__(self, index_or_slice: int | slice) -> T | Sequence[T]:
        result = self.__data[index_or_slice]
        if not isinstance(index_or_slice, slice):
            return result
        return List(result)

    def __len__(self) -> int:
        return len(self.__data)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, List):
            return False
        return self.__data == other.__data

    def cast(self, new_type: Type[T2]) -> List[T2]:
        return self.map(cast(new_type))

    def map(self, function: Callable[[T], T2]) -> List[T2]:
        return List(map(function, self))

    def filter(self, function: Callable[[T], bool]) -> List[T]:
        return List(filter(function, self))

    def refine(self, new_type: Type[T2], function: Callable[[T], bool]) -> List[T2]:
        return List(filter(function, self)) \
            .cast(new_type)

    @overload
    def reduce(self, function: Callable[[T, T], T]) -> T: ...

    @overload
    def reduce(self, function: Callable[[T2, T], T2], initial: T2) -> T2: ...

    def reduce(self, function: Callable, initial: T2 = None) -> T | T2:
        if initial is None:
            return reduce(function, self)
        return reduce(function, self, initial)

    def find_first_map(self, function: Callable[[T], Maybe[T2]]) -> Maybe[T2]:
        for element in self:
            maybe_result = function(element)
            if maybe_result.is_some:
                return maybe_result
        return Nothing

    def add(self, element: T) -> List[T]:
        new_data = self.__data + (element,)
        return List(new_data)

    def delete_at(self, index: int) -> Either[IndexError, List[T]]:
        if index >= len(self.__data) or index < -len(self.__data):
            return Left(IndexError(f'index {index} is of out range'))
        normalized_index = index if index >= 0 else len(self.__data) + index
        new_data = (element for element_index, element in enumerate(self.__data) if element_index != normalized_index)
        return Right(List(new_data))

    def delete_at_unsafe(self, index: int) -> List[T]:
        return self.delete_at(index).get_or_raise()

    def pop(self, index: int = None) -> Either[IndexError, tuple[T, List[T]]]:
        if len(self.__data) == 0:
            return Left(IndexError('list is empty'))
        if index is not None and (index >= len(self.__data) or index < -len(self.__data)):
            return Left(IndexError(f'index {index} is of out range'))
        normalized_index = index if index is not None else -1
        element = self.__data[normalized_index]
        new_list = self.delete_at_unsafe(normalized_index)
        return Right((element, new_list))

    def pop_unsafe(self, index: int = None) -> tuple[T, List[T]]:
        return self.pop(index).get_or_raise()

    def __str__(self) -> str:
        elements = ', '.join(map(str, self))
        return f'List([{elements}])'
