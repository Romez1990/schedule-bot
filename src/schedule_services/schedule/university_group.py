from __future__ import annotations
from data.fp.maybe import Maybe

from .education_form import EducationForm
from .group import Group


class UniversityGroup(Group):
    def __init__(self, speciality: str, year: int, form: str, number: Maybe[int]) -> None:
        self.speciality = speciality
        self.year = year
        self.form = EducationForm(form)
        self.number = number
        self.str = self.__get_str()

    def __get_str(self) -> str:
        number_or_nothing = self.number.map(str).get_or('')
        return f'{self.speciality}-{self.year}-{self.form}{number_or_nothing}'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, UniversityGroup):
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
        # if self.year < other.year:
            return True
        if self.year != other.year:
            return False
        if self.speciality < other.speciality:
            return True
        if self.speciality != other.speciality:
            return False
        if self.number.get_or(0) < other.number.get_or(0):
            return True
        return False

    # def __gt__(self, other: UniversityGroup) -> bool:
    #     return self != other and not self < other

    def __hash__(self) -> int:
        return hash(str(self))

    def __str__(self) -> str:
        return self.str
