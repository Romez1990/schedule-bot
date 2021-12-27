from collections.abc import Sequence
from typing import (
    Iterable,
)

from data.fp.maybe import Maybe, Nothing
from .entry import Entry


class DaySchedule(Sequence[Maybe[Entry]]):
    def __init__(self, entries: Iterable[Maybe[Entry]]) -> None:
        self.__entries = tuple(entries)

    def __getitem__(self, index: int) -> Maybe[Entry]:
        return self.__entries[index]

    def __len__(self) -> int:
        return len(self.__entries)

    def is_empty(self) -> bool:
        return all(entry == Nothing for entry in self.__entries)
