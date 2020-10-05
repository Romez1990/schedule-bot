from typing import (
    Iterable,
    Iterator,
    Reversible,
)
from pyrsistent import pvector
from returns.maybe import Maybe, Nothing

from .entry import Entry


class DaySchedule(Reversible[Maybe[Entry]]):
    def __init__(self, entries: Iterable[Maybe[Entry]]) -> None:
        self.__entries = pvector(entries)

    def __iter__(self) -> Iterator[Maybe[Entry]]:
        return iter(self.__entries)

    def __reversed__(self) -> Iterator[Maybe[Entry]]:
        return iter(reversed(self.__entries))

    def __bool__(self) -> bool:
        return not all(entry == Nothing for entry in self.__entries)
