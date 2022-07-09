from abc import ABCMeta, abstractmethod
from typing import (
    Type,
    TypeVar,
)

T = TypeVar('T')


class JsonSerializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, value: object, *, ensure_ascii=True) -> str: ...

    @abstractmethod
    def deserialize(self, data: str, *, value_type: Type[T]) -> T: ...
