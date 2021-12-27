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
from data.fp.type import cast

T = TypeVar('T')
T2 = TypeVar('T2')


class List(Sequence[T]):
    def __init__(self, iterable: Iterable[T] = None) -> None:
        self.__data = self.__create_list(iterable)

    def __create_list(self, iterable: Optional[Iterable[T]]) -> tuple[T]:
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
        if not isinstance(result, list):
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

    @overload
    def reduce(self, function: Callable[[T, T], T]) -> T: ...

    @overload
    def reduce(self, function: Callable[[T2, T], T2], initial: T2) -> T2: ...

    def reduce(self, function: Callable, initial: T2 = None) -> T | T2:
        if initial is None:
            return reduce(function, self)
        return reduce(function, self, initial)

    def add(self, element: T) -> List[T]:
        new_data = list(self.__data)
        new_data.append(element)
        return List(new_data)

    def remove(self, element: T) -> Either[ValueError, List[T]]:
        new_data = list(self.__data)
        try:
            new_data.remove(element)
        except ValueError:
            return Left(ValueError(f'{element} not in list'))
        return Right(List(new_data))

    def remove_unsafe(self, element: T) -> List[T]:
        return self.remove(element).get_or_raise()

    def remove_at(self, index: int) -> Either[IndexError, List[T]]:
        new_data = list(self.__data)
        try:
            del new_data[index]
        except IndexError:
            return Left(IndexError(f'index {index} is of out range'))
        return Right(List(new_data))

    def remove_at_unsafe(self, index: int) -> List[T]:
        return self.remove_at(index).get_or_raise()

    def pop(self, index: int = None) -> tuple[T, List[T]]:
        new_data = list(self.__data)
        element = new_data.pop() if index is None else new_data.pop(index)
        return element, List(new_data)

    def __str__(self) -> str:
        return str(self.__data)
