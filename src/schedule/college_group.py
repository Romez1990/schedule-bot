from __future__ import annotations
from .group import Group


class CollegeGroup(Group):
    def __init__(self, year: int, speciality: str, number: int, a: bool, admission_year: int) -> None:
        self.__year = year
        self.__speciality = speciality.upper()
        self.__number = number
        self.__a = a
        self.__admission_year = admission_year

    @property
    def year(self) -> int:
        return self.__year

    @property
    def speciality(self) -> str:
        return self.__speciality

    @property
    def number(self) -> int:
        return self.__number

    @property
    def a(self) -> bool:
        return self.__a

    @property
    def admission_year(self) -> int:
        return self.__admission_year

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CollegeGroup):
            return self.year == other.year and \
                   self.speciality == other.speciality and \
                   self.number == other.number and \
                   self.a == other.a and \
                   self.admission_year == other.admission_year

        raise NotImplemented

    def __lt__(self, other: CollegeGroup) -> bool:
        if self.year < other.year:
            return True
        if self.year != other.year:
            return False
        if self.number < other.number:
            return True
        if self.number != other.number:
            return False
        if not self.a and other.a:
            return True
        return False

    def __gt__(self, other: CollegeGroup) -> bool:
        return self != other and not self < other

    def __str__(self) -> str:
        a = 'а' if self.a else ''
        return f'{self.year}{self.speciality}-{self.number}{a}.{self.admission_year}'

    def __hash__(self) -> int:
        return hash(str(self))
