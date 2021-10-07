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

from data.fp.type import cast

T = TypeVar('T')
T2 = TypeVar('T2')


class List(Sequence[T]):
    def __init__(self, iterable: Iterable[T] = None) -> None:
        self.__list = self.__create_list(iterable)

    def __create_list(self, iterable: Optional[Iterable[T]]) -> list[T]:
        if iterable is None:
            return []
        if isinstance(iterable, List):
            return iterable.__list
        return list(iterable)

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, slice_: slice) -> Sequence[T]: ...

    def __getitem__(self, index_or_slice: int | slice) -> T | Sequence[T]:
        result = self.__list[index_or_slice]
        if not isinstance(result, list):
            return result
        return List(result)

    def __len__(self) -> int:
        return len(self.__list)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, List):
            return False
        return self.__list == other.__list

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
        new_list = self.__list.copy()
        new_list.append(element)
        return List(new_list)

    def remove(self, element: T) -> List[T]:
        new_list = self.__list.copy()
        try:
            new_list.remove(element)
        except ValueError:
            raise ValueError(f'{element} not in list')
        return List(new_list)

    def pop(self, index: int = None) -> tuple[T, List[T]]:
        new_list = self.__list.copy()
        element = new_list.pop() if index is None else new_list.pop(index)
        return element, List(new_list)

    def __str__(self) -> str:
        return str(self.__list)
