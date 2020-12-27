from __future__ import annotations
from functools import reduce
from typing import (
    Callable,
    Collection,
    Iterable,
    Iterator,
    TypeVar,
)

A = TypeVar('A')
B = TypeVar('B')


class List(Collection[A]):
    def __init__(self, iterable: Iterable[A] = None) -> None:
        self.__list: list[A] = list(iterable) if iterable is not None else []

    def __iter__(self) -> Iterator[A]:
        return iter(self.__list)

    def __len__(self) -> int:
        return len(self.__list)

    def __contains__(self, element: A) -> bool:
        return element in self.__list

    def __getitem__(self, index: int) -> A:
        return self.__list[index]

    def __eq__(self, other: List[A]) -> bool:
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self[i] != other[i]:
                return False
        return True

    def map(self, function: Callable[[A], B]) -> List[B]:
        return List(map(function, self))

    def filter(self, function: Callable[[A], bool]) -> List[A]:
        return List(filter(function, self))

    def reduce(self, function: Callable[[B, A], B], initial: B = None) -> B:
        if initial is None:
            return reduce(function, self)
        return reduce(function, self, initial)

    def add(self, element: A) -> List[A]:
        new_list = self.__list.copy()
        new_list.append(element)
        return List(new_list)

    def remove(self, element: A) -> List[A]:
        new_list = self.__list.copy()
        try:
            new_list.remove(element)
        except ValueError:
            raise ValueError(f'{element} not in list')
        return List(new_list)

    def pop(self, index: int = None) -> tuple[A, List[A]]:
        new_list = self.__list.copy()
        element = new_list.pop(index)
        return element, List(new_list)
