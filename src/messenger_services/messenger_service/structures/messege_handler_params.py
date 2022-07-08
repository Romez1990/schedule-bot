from __future__ import annotations
from dataclasses import dataclass
from typing import (
    Type,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from messenger_services.messenger_service.messenger_controller import MessengerController


@dataclass(frozen=True, eq=False)
class MessageHandlerParams:
    controller_class: Type[MessengerController]
    method_name: str
    command: str
