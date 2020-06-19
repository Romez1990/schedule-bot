from typing import List, Optional, Iterator

from utils.hashing import hash_somehow
from .entry import Entry


class DaySchedule:
    def __init__(self, entries: List[Optional[Entry]] = None):
        self._entries: List[Optional[Entry]] = \
            [] if entries is None else entries

    def append(self, entry: Optional[Entry]) -> None:
        self._entries.append(entry)

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self) -> Iterator[Optional[Entry]]:
        return iter(self._entries)

    def __bool__(self) -> bool:
        return all([
            self._entries,
            any([entry for entry in self._entries]),
        ])

    __nonzero__ = __bool__

    def __hash__(self) -> int:
        return hash_somehow(str([hash(entry) for entry in self._entries]))
