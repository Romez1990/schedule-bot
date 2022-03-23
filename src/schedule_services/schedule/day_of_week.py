from __future__ import annotations
from enum import Enum, auto


class DayOfWeek(Enum):
    monday = auto()
    tuesday = auto()
    wednesday = auto()
    thursday = auto()
    friday = auto()
    saturday = auto()
    sunday = auto()

    def __repr__(self) -> str:
        return f'DayOfWeek.{self.name}'
