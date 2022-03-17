from functools import reduce
from typing import (
    Callable,
    TypeVar,
    overload,
)

from .list import List

A = TypeVar('A')
B = TypeVar('B')


@overload
def lazy_reduce(function: Callable[[A, Callable[[], A]], A], lazy_list: List[Callable[[], A]]) -> A: ...


@overload
def lazy_reduce(function: Callable[[B, Callable[[], A]], B], lazy_list: List[Callable[[], A]],
                initial: B) -> B: ...


def lazy_reduce(function: Callable, lazy_list: List[Callable[[], A]], initial: B = None) -> A | B:
    if initial is not None:
        return reduce(function, lazy_list, initial)
    head, tail = lazy_list.pop_unsafe(0)
    return reduce(function, tail, head())
