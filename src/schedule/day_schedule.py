from typing import (
    Iterable,
    Iterator,
    Reversible,
    Sized,
)
from returns.maybe import Maybe, Nothing

from src.immutable_collections import (
    List,
)
from .entry import Entry


class DaySchedule(Reversible[Maybe[Entry]], Sized):
    def __init__(self, entries: Iterable[Maybe[Entry]]) -> None:
        self.__entries = List(entries)

    def __iter__(self) -> Iterator[Maybe[Entry]]:
        return iter(self.__entries)

    def __len__(self) -> int:
        return len(self.__entries)

    def __reversed__(self) -> Iterator[Maybe[Entry]]:
        return iter(reversed(self.__entries))

    def __bool__(self) -> bool:
        return any(entry != Nothing for entry in self.__entries)
