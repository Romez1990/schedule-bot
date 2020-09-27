from typing import (
    Type,
    Dict,
    TypeVar,
)

from .errors import TypeNotFoundError

T = TypeVar('T')


class Container:
    def __init__(self, types: Dict[Type, object]) -> None:
        self.__types: Dict[Type, object] = types

    def get(self, base_type: Type[T]) -> T:
        if base_type not in self.__types:
            raise TypeNotFoundError(base_type)
        return self.__types[base_type]
