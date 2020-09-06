from __future__ import annotations
from enum import Enum


class WeekDay(Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6

    def __gt__(self, other: WeekDay) -> bool:
        return self.value > other.value

    def __lt__(self, other: WeekDay) -> bool:
        return self.value < other.value
