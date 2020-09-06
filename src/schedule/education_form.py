from __future__ import annotations
from typing import Tuple


class EducationForm:
    def __init__(self, form: str) -> None:
        self.__form = form

    def __eq__(self, other: object) -> bool:
        if isinstance(other, EducationForm):
            return str(self) == str(other)

        raise NotImplemented

    def __gt__(self, other: EducationForm) -> bool:
        self_index, other_index = self.__get_compare_indexes(other)
        return self_index > other_index

    def __lt__(self, other: EducationForm) -> bool:
        self_index, other_index = self.__get_compare_indexes(other)
        return self_index < other_index

    __forms = ['Д', 'В']

    def __get_compare_indexes(self, other: EducationForm) -> Tuple[int, int]:
        self_char = str(self)[0].upper()
        other_char = str(other)[0].upper()
        self_index = self.__forms.index(self_char)
        other_index = self.__forms.index(other_char)
        return self_index, other_index

    def __str__(self) -> str:
        return self.__form
