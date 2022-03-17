from abc import ABCMeta, abstractmethod
from typing import (
    Type,
    TypeVar,
)

T = TypeVar('T')


class BytesSerializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, value: object) -> bytes: ...

    @abstractmethod
    def deserialize(self, value: bytes, object_type: Type[T]) -> T: ...
