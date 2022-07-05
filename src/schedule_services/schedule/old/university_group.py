from __future__ import annotations
from data.fp.maybe import Maybe
from .education_form import EducationForm


class UniversityGroup:
    def __init__(self, speciality: str, year: int, form: str, number: Maybe[int]) -> None:
        self.speciality = speciality
        self.year = year
        self.form = EducationForm(form)
        self.number = number

    def __get_attributes(self) -> list[object]:
        return [
            self.speciality,
            self.year,
            self.form,
            self.number,
        ]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, UniversityGroup):
            return self.__get_attributes() == other.__get_attributes()
        raise NotImplemented

    def __lt__(self, other: UniversityGroup) -> bool:
        return (self.form, -self.year, self.speciality, self.number.get_or(0)) < \
               (other.form, -other.year, other.speciality, other.number.get_or(0))

    def __hash__(self) -> int:
        return hash(self.__get_attributes())

    def __str__(self) -> str:
        number_or_nothing = self.number.map(str).get_or('')
        return f'{self.speciality}-{self.year}-{self.form}{number_or_nothing}'
