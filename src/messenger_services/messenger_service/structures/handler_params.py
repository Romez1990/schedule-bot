from __future__ import annotations
from dataclasses import dataclass
from typing import (
    Type,
    TYPE_CHECKING,
)

from .payload import Payload

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


@dataclass(frozen=True, eq=False)
class CallbackHandlerParams:
    payload_class: Type[Payload]


@dataclass(frozen=True, eq=False)
class CallbackHandlerParamsForRegistrar(CallbackHandlerParams, HandlerParamsForRegistrar):
    pass
