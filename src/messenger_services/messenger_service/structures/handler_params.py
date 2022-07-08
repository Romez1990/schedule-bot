from __future__ import annotations
from dataclasses import dataclass
from typing import (
    Type,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from messenger_services.messenger_service.messenger_controller import MessengerController


@dataclass(frozen=True, eq=False)
class HandlerParamsForRegistrar:
    controller_class: Type[MessengerController]
    method_name: str


@dataclass(frozen=True, eq=False)
class MessageHandlerParams:
    command: str


@dataclass(frozen=True, eq=False)
class MessageHandlerParamsForRegistrar(MessageHandlerParams, HandlerParamsForRegistrar):
    pass
