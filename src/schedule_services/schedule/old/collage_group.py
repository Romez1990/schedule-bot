from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CollegeGroup:
    year: int
    speciality: str
    number: int
    a: bool
    admission_year: int

    def __lt__(self, other: CollegeGroup) -> bool:
        return (self.year, self.number, self.a) < \
               (other.year, other.number, other.a)

    def __str__(self) -> str:
        a = 'а' if self.a else ''
        return f'{self.year}{self.speciality}-{self.number}{a}.{self.admission_year}'
