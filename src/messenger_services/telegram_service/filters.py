from typing import (
    Mapping,
    Type,
)
from aiogram.dispatcher.filters import (
    Filter,
)
from aiogram.types import (
    CallbackQuery,
)

from data.serializers import JsonSerializer
from messenger_services.messenger_service import (
    Payload,
)


class CallbackPayloadFilter(Filter):
    def __init__(self, json_serializer: JsonSerializer, payload_class: Type[Payload]) -> None:
        self.__json_serializer = json_serializer
        self.__payload_class = payload_class

    async def check(self, query: CallbackQuery) -> bool:
        data = self.__json_serializer.deserialize(query.data, value_type=Mapping)
        return data['type'] == self.__payload_class.type
