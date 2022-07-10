from typing import (
    Type,
    MutableMapping,
)

from infrastructure.ioc_container import service
from messenger_services.messenger_service import (
    Payload,
)
from .payload_classes_repository import PayloadClassesRepository


@service
class PayloadClassesRepositoryImpl(PayloadClassesRepository):
    def __init__(self) -> None:
        self.__payloads: MutableMapping[str, Type[Payload]] = {}

    def save(self, payload_class: Type[Payload]) -> None:
        self.__payloads[payload_class.type] = payload_class

    def get_by_type(self, payload_type: str) -> Type[Payload]:
        return self.__payloads[payload_type]
