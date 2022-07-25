from typing import (
    Mapping,
    MutableMapping,
)

from infrastructure.ioc_container import service
from data.serializers import JsonSerializer
from .structures import (
    Payload,
)
from .payload_classes_repository import PayloadClassesRepository
from .payload_serializer import PayloadSerializer


@service
class PayloadSerializerImpl(PayloadSerializer):
    def __init__(self, payload_classes: PayloadClassesRepository, json_serializer: JsonSerializer) -> None:
        self.__payload_classes = payload_classes
        self.__json_serializer = json_serializer

    def serialize(self, payload: Payload) -> str:
        payload_dict = payload.__dict__
        payload_dict['type'] = payload.type
        return self.__json_serializer.serialize(payload_dict, ensure_ascii=False)

    def deserialize_from_json(self, data: str) -> Payload:
        data_dict = self.__json_serializer.deserialize(data, value_type=MutableMapping)
        return self.__deserialize_from_mutable_dict(data_dict)

    def deserialize_from_dict(self, data: Mapping[str, object]) -> Payload:
        data_copy = dict(data)
        return self.__deserialize_from_mutable_dict(data_copy)

    def __deserialize_from_mutable_dict(self, data: MutableMapping[str, object]) -> Payload:
        payload_type = data['type']
        if not isinstance(payload_type, str):
            raise RuntimeError
        payload_class = self.__payload_classes.find_by_type(payload_type)
        del data['type']
        return payload_class(**data)
