from typing import (
    Iterable,
    Iterator,
)
from pyrsistent import pvector
from returns.maybe import Maybe

from .entry import Entry


class DaySchedule(Iterable[Maybe[Entry]]):
    def __init__(self, entries: Iterable[Maybe[Entry]]):
        self.__entries = pvector(entries)

    def __iter__(self) -> Iterator[Maybe[Entry]]:
        return iter(self.__entries)
