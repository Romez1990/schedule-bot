from typing import (
    Type,
)

from data.serializers import JsonSerializer
from messenger_services.messenger_service import (
    Callback,
    Payload,
)
from .filter import Filter


class CallbackPayloadFilter(Filter):
    def __init__(self, json_serializer: JsonSerializer, payload_class: Type[Payload]) -> None:
        self.__json_serializer = json_serializer
        self.__payload_class = payload_class

    def check(self, callback: Callback) -> bool:
        return callback.payload.type == self.__payload_class.type
