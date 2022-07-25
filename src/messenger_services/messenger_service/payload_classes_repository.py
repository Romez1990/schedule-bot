from abc import ABCMeta, abstractmethod
from typing import (
    Type,
    Sequence,
)

from messenger_services.messenger_service import (
    Payload,
)


class PayloadClassesRepository(metaclass=ABCMeta):
    @abstractmethod
    def save(self, payload_class: Type[Payload]) -> None: ...

    @abstractmethod
    def find_by_type(self, payload_type: str) -> Type[Payload]: ...
