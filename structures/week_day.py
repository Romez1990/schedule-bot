from __future__ import annotations
from enum import Enum

from bidict import bidict


class WeekDay(Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6

    def translate(self) -> str:
        return dictionary[self]

    @staticmethod
    def from_text(week_day: str) -> WeekDay:
        return dictionary.inverse[week_day]

    def __lt__(self, other: Enum) -> bool:
        return self.value < other.value


dictionary = bidict({
    WeekDay.monday: 'Понедельник',
    WeekDay.tuesday: 'Вторник',
    WeekDay.wednesday: 'Среда',
    WeekDay.thursday: 'Четверг',
    WeekDay.friday: 'Пятница',
    WeekDay.saturday: 'Суббота',
    WeekDay.sunday: 'Воскресение',
})
