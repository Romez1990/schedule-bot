from __future__ import annotations

import re


class Group:
    def __init__(self, group_name: str):
        result = re.search(
            '^([1-4])([А-Яа-я]{2,4})-(\\d{1,2})(а?)\\.?(\\d{2})$',
            group_name)
        if result is None:
            raise ValueError(f'Cannot parse this group name: {group_name}')
        self.grade = int(result.group(1))
        self.specialty = result.group(2)
        self.number = int(result.group(3))
        self.a = bool(result.group(4))
        self.admission_year = int(result.group(5))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Group):
            return all([
                self.grade == other.grade,
                self.specialty == other.specialty,
                self.number == other.number,
                self.a == other.a,
                self.admission_year == other.admission_year,
            ])

        raise NotImplemented

    def __gt__(self, other: Group) -> bool:
        return any([
            self.grade > other.grade,
            self.number > other.number,
            self.a and not other.a,
        ])

    def __lt__(self, other: Group) -> bool:
        return any([
            self.grade < other.grade,
            self.number < other.number,
            not self.a and other.a,
        ])

    def __str__(self) -> str:
        a = 'а' if self.a else ''
        return f'{self.grade}{self.specialty}-' \
               f'{self.number}{a}.{self.admission_year}'

    def __hash__(self) -> int:
        return hash(str(self))
