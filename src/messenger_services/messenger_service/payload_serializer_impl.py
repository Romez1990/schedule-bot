from typing import (
    Mapping,
    MutableMapping,
    Type,
)

from infrastructure.ioc_container import service
from data.serializers import JsonSerializer
from .structures import (
    Payload,
)
from .payload_serializer import PayloadSerializer


@service
class PayloadSerializerImpl(PayloadSerializer):
    def __init__(self, json_serializer: JsonSerializer) -> None:
        self.__json_serializer = json_serializer

    def serialize(self, payload: Payload) -> str:
        payload_dict = payload.__dict__
        payload_dict['type'] = payload.type
        return self.__json_serializer.serialize(payload_dict, ensure_ascii=False)

    def deserialize(self, data: str, payload_classes: Mapping[str, Type[Payload]]) -> Payload:
        data_dict = self.__json_serializer.deserialize(data, value_type=MutableMapping)
        payload_type = data_dict['type']
        payload_class = payload_classes[payload_type]
        del data_dict['type']
        return payload_class(**data_dict)
