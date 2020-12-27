from __future__ import annotations
from typing import (
    Iterator,
    Mapping,
    TypeVar,
)

from .list import List

KA = TypeVar('KA')
VA = TypeVar('VA')


class Dict(Mapping[KA, VA]):
    def __init__(self, mapping: Mapping[KA, VA] = None) -> None:
        self.__dict: dict[KA, VA] = dict(mapping) if mapping is not None else {}

    def __iter__(self) -> Iterator[KA]:
        return iter(self.__dict)

    def __getitem__(self, key: KA) -> VA:
        return self.__dict[key]

    def __len__(self) -> int:
        return len(self.__dict)

    def __contains__(self, key: KA) -> bool:
        return key in self.__dict

    def get(self, key: KA) -> VA:
        return self.__dict.get(key)

    def keys(self) -> List[KA]:
        return List(self.__dict.keys())

    def values(self) -> List[VA]:
        return List(self.__dict.values())

    def items(self) -> List[tuple[KA, VA]]:
        return List(self.__dict.items())

    def __eq__(self, other: Dict[KA, VA]) -> bool:
        self_keys = set(self.keys())
        other_keys = set(other.keys())
        if self_keys != other_keys:
            return False
        for key in self_keys:
            if self[key] != other[key]:
                return False
        return True

    def add(self, key: KA, value: VA) -> Dict[KA, VA]:
        new_dict = self.__dict.copy()
        new_dict[key] = value
        return Dict(new_dict)

    def remove(self, key: KA) -> Dict[KA, VA]:
        new_dict = self.__dict.copy()
        try:
            del new_dict[key]
        except KeyError:
            raise KeyError(key)
        return Dict(new_dict)
