from functools import reduce
from typing import (
    Callable,
    TypeVar,
)

from src.immutable_collections import (
    List,
)

A = TypeVar('A')
B = TypeVar('B')


def lazy_reduce(function: Callable[[B, Callable[[], A]], B], list: List[Callable[[], A]], initial: B = None):
    if initial is not None:
        return reduce(function, list, initial)
    head, tail = list.pop(0)
    return reduce(function, tail, head())
