from __future__ import annotations
from functools import reduce
from collections.abc import Sequence
from typing import (
    Callable,
    Iterable,
    Type,
    TypeVar,
    overload,
    cast,
)

from data.fp.either import Either, Right, Left
from data.fp.maybe import Maybe, Nothing

T = TypeVar('T')
T2 = TypeVar('T2')
TResult = TypeVar('TResult')


class List(Sequence[T]):
    def __init__(self, iterable: Iterable[T] = None) -> None:
        self.__data = self.__create_list(iterable)

    def __create_list(self, iterable: Iterable[T] | None) -> tuple[T, ...]:
        if iterable is None:
            return tuple()
        if isinstance(iterable, List):
            return iterable.__data
        return tuple(iterable)

    @staticmethod
    def zip(elements_1: Iterable[T], elements_2: Iterable[T2]) -> List[tuple[T, T2]]:
        return List(zip(elements_1, elements_2))

    @staticmethod
    def unzip(self: Iterable[tuple[T, T2]]) -> tuple[List[T], List[T2]]:
        def create_list(t: tuple[TResult, ...]) -> List[TResult]:
            return List(t)

        result = List(zip(*self)) \
            .map(create_list)
        return cast(tuple[List[T], List[T2]], tuple(result))

    @staticmethod
    def flatten(self: Iterable[Iterable[T]]) -> List[T]:
        return List(element for sub_list in self for element in sub_list)

    @staticmethod
    def filter_map(self: Iterable[T], mapper: Callable[[T], Maybe[TResult]]) -> List[TResult]:
        result: list[TResult] = []

        def add_value(value: TResult) -> None:
            result.append(value)

        for element in self:
            mapper(element) \
                .map(add_value)
        return List(result)

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, slice_: slice) -> Sequence[T]: ...

    def __getitem__(self, index_or_slice: int | slice) -> T | Sequence[T]:
        result = self.__data[index_or_slice]
        if isinstance(index_or_slice, slice):
            if not isinstance(result, tuple):
                raise RuntimeError
            return List(result)
        return result

    def __len__(self) -> int:
        return len(self.__data)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, List):
            return self.__data == other.__data
        if isinstance(other, list):
            return list(self.__data) == other
        if isinstance(other, tuple):
            return self.__data == other
        return False

    def cast(self, _: Type[TResult]) -> List[TResult]:
        return cast(List[TResult], self)

    def map(self, function: Callable[[T], TResult]) -> List[TResult]:
        return List(map(function, self))

    def filter(self, function: Callable[[T], bool]) -> List[T]:
        return List(filter(function, self))

    def refine(self, new_type: Type[TResult], function: Callable[[T], bool]) -> List[TResult]:
        return List(filter(function, self)) \
            .cast(new_type)

    @overload
    def reduce(self, function: Callable[[T, T], T]) -> T: ...

    @overload
    def reduce(self, function: Callable[[TResult, T], TResult], initial: TResult) -> TResult: ...

    def reduce(self, function: Callable, initial: TResult = None) -> T | TResult:
        if initial is None:
            return reduce(function, self)
        return reduce(function, self, initial)

    def find_first_map(self, function: Callable[[T], Maybe[TResult]]) -> Maybe[TResult]:
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

    def __repr__(self) -> str:
        elements = ', '.join(map(str, self))
        return f'List([{elements}])'
