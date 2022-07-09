from typing import (
    Type,
    TypeVar,
)
import pickle

from infrastructure.ioc_container import service
from .bytes_serializer import BytesSerializer

T = TypeVar('T')


@service
class BytesSerializerImpl(BytesSerializer):
    def serialize(self, value: object) -> bytes:
        return pickle.dumps(value)

    def deserialize(self, value_bytes: bytes, object_type: Type[T]) -> T:
        return pickle.loads(value_bytes)
