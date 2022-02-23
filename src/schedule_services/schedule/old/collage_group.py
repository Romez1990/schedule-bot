from __future__ import annotations


class CollegeGroup:
    def __init__(self, year: int, speciality: str, number: int, a: bool, admission_year: int) -> None:
        self.year = year
        self.speciality = speciality
        self.number = number
        self.a = a
        self.admission_year = admission_year

    def __get_attributes(self) -> list[object]:
        return [
            self.year,
            self.speciality,
            self.number,
            self.a,
            self.admission_year,
        ]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, CollegeGroup):
            return self.__get_attributes() == other.__get_attributes()
        raise NotImplemented

    def __lt__(self, other: CollegeGroup) -> bool:
        return (self.year, self.number, self.a) < \
               (other.year, other.number, other.a)

    def __hash__(self) -> int:
        return hash(self.__get_attributes())

    def __str__(self) -> str:
        a = 'а' if self.a else ''
        return f'{self.year}{self.speciality}-{self.number}{a}.{self.admission_year}'
