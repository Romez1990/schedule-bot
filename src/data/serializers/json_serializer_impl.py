from typing import (
    Type,
    TypeVar,
)
import json

from infrastructure.ioc_container import service
from .json_serializer import JsonSerializer

T = TypeVar('T')


@service
class JsonSerializerImpl(JsonSerializer):
    def serialize(self, value: object, *, ensure_ascii: bool = True) -> str:
        return json.dumps(value, ensure_ascii=ensure_ascii)

    def deserialize(self, data: str, *, value_type: Type[T]) -> T:
        return json.loads(data)
