from __future__ import annotations
import re


class Group:
    def __init__(self, group_name: str):
        result = re.search(
            '^(?P<grade>[1-4])(?P<specialty>[А-Яа-я]{2,4})-'
            '(?P<number>\\d{1,2})(?P<a>а?)\\.?(?P<admission_year>\\d{2})$',
            group_name)
        if result is None:
            raise ValueError(f'Cannot parse this group name: {group_name}')
        self.grade = int(result.group('grade'))
        self.specialty = result.group('specialty')
        self.number = int(result.group('number'))
        self.a = bool(result.group('a'))
        self.admission_year = int(result.group('admission_year'))

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
