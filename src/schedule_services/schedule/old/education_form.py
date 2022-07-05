from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class EducationForm:
    form: str

    def __post_init__(self) -> None:
        if not self.form.isupper():
            raise ValueError(f'form must be upper, got {self.form}')

    def __lt__(self, other: EducationForm) -> bool:
        self_index, other_index = self.__get_compare_indexes(other)
        return self_index < other_index

    __forms = ['Д', 'В']

    def __get_compare_indexes(self, other: EducationForm) -> tuple[int, int]:
        self_char = str(self)[0]
        other_char = str(other)[0]
        self_index = self.__forms.index(self_char)
        other_index = self.__forms.index(other_char)
        return self_index, other_index

    def __str__(self) -> str:
        return self.form
