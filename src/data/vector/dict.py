from __future__ import annotations
from collections.abc import Mapping
from typing import (
    Iterator,
    Callable,
    Type,
    TypeVar,
)

from data.fp.type import cast

K = TypeVar('K')
K2 = TypeVar('K2')
V = TypeVar('V')
V2 = TypeVar('V2')


class Dict(Mapping[K, V]):
    def __init__(self, mapping: Mapping[K, V] = None) -> None:
        self.__dict: dict[K, V] = dict(mapping) if mapping is not None else {}

    def __iter__(self) -> Iterator[K]:
        return iter(self.__dict)

    def __len__(self) -> int:
        return len(self.__dict)

    def __getitem__(self, key: K) -> V:
        return self.__dict[key]

    def cast(self, new_type: Type[V2]) -> Dict[K, V2]:
        return self.map(cast(new_type))

    def map(self, fn: Callable[[V], V2]) -> Dict[K, V2]:
        new_dict = {}
        for key, value in self.__dict.items():
            new_dict[key] = fn(value)
        return Dict(new_dict)

    def add(self, key: K, value: V) -> Dict[K, V]:
        new_dict = self.__dict.copy()
        new_dict[key] = value
        return Dict(new_dict)

    def remove(self, key: K) -> Dict[K, V]:
        new_dict = self.__dict.copy()
        try:
            del new_dict[key]
        except KeyError:
            raise KeyError(key)
        return Dict(new_dict)

    def __str__(self) -> str:
        return str(self.__dict)
