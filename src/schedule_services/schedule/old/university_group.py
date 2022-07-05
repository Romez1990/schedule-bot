from __future__ import annotations
from dataclasses import dataclass

from data.fp.maybe import Maybe
from .education_form import EducationForm


@dataclass(frozen=True)
class UniversityGroup:
    speciality: str
    year: int
    form: EducationForm
    number: Maybe[int]

    def __post_init__(self) -> None:
        if not self.speciality.isupper():
            raise ValueError(f'speciality must be upper, got {self.form}')

    def __lt__(self, other: UniversityGroup) -> bool:
        return (self.form, -self.year, self.speciality, self.number.get_or(0)) < \
               (other.form, -other.year, other.speciality, other.number.get_or(0))

    def __str__(self) -> str:
        number_or_nothing = self.number.map(str).get_or('')
        return f'{self.speciality}-{self.year}-{self.form}{number_or_nothing}'
