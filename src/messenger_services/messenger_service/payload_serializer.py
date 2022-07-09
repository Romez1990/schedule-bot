from abc import ABCMeta, abstractmethod
from typing import (
    Mapping,
    Type,
)

from .structures import (
    Payload,
)


class PayloadSerializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, payload: Payload) -> str: ...

    @abstractmethod
    def deserialize(self, data: str, payload_classes: Mapping[str, Type[Payload]]) -> Payload: ...
