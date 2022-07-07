from dataclasses import dataclass
from typing import (
    ClassVar,
)

from messenger_services.messenger_service import (
    Payload,
)


@dataclass(frozen=True, eq=False)
class DeleteGroupPayload(Payload):
    type: ClassVar[str] = 'delete_group'
    group: str
