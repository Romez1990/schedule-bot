from __future__ import annotations
from typing import (
    Type,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from .messenger_controller import MessengerController


class MessageHandlerParameters:
    def __init__(self, controller_class: Type[MessengerController], method_name: str, command: str) -> None:
        self.controller_class = controller_class
        self.method_name = method_name
        self.command = command
