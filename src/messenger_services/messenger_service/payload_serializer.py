from abc import ABCMeta, abstractmethod
from typing import (
    Mapping,
)

from .structures import (
    Payload,
)


class PayloadSerializer(metaclass=ABCMeta):
    @abstractmethod
    def serialize(self, payload: Payload) -> str: ...

    @abstractmethod
    def deserialize_from_json(self, data: str) -> Payload: ...

    @abstractmethod
    def deserialize_from_dict(self, data: Mapping[str, object]) -> Payload: ...
