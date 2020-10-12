from __future__ import annotations
from returns.maybe import Maybe

from .education_form import EducationForm
from .group import Group


class UniversityGroup(Group):
    def __init__(self, speciality: str, year: int, form: str, number: Maybe[int]) -> None:
        self.__speciality = speciality.upper()
        self.__year = year
        self.__form = EducationForm(form)
        self.__number = number

    @property
    def speciality(self) -> str:
        return self.__speciality

    @property
    def year(self) -> int:
        return self.__year

    @property
    def form(self) -> EducationForm:
        return self.__form

    @property
    def number(self) -> Maybe[int]:
        return self.__number

    def __eq__(self, other: object) -> bool:
        if type(other) == UniversityGroup:
            return self.speciality == other.speciality and \
                   self.year == other.year and \
                   self.form == other.form and \
                   self.number == other.number

        raise NotImplemented

    def __lt__(self, other: UniversityGroup) -> bool:
        if self.form < other.form:
            return True
        if self.form != other.form:
            return False
        if self.year > other.year:
            return True
        if self.year != other.year:
            return False
        if self.speciality < other.speciality:
            return True
        if self.speciality != other.speciality:
            return False
        if self.number.value_or(0) < other.number.value_or(0):
            return True
        return False

    def __gt__(self, other: UniversityGroup) -> bool:
        return self != other and not self < other

    def __str__(self) -> str:
        number = self.number.value_or('')
        return f'{self.speciality}-{self.year}-{self.form}{number}'

    def __hash__(self) -> int:
        return hash(str(self))
