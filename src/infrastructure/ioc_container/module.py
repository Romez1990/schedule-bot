from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import (
    TYPE_CHECKING,
)

from .binding_context import BindingContext

if TYPE_CHECKING:
    from .container import Container


class Module(metaclass=ABCMeta):
    def __init__(self, container: Container) -> None:
        self.__container = container

    @abstractmethod
    def load(self) -> None: ...

    def _bind(self, class_type: type) -> BindingContext:
        def bind_to_base_class(base_class: type | None, to_self: bool) -> None:
            if to_self:
                self.__container.bind(class_type).to_self()
            else:
                if base_class is None:
                    raise RuntimeError('base class is None')
                self.__container.bind(class_type).to(base_class)

        return BindingContext(bind_to_base_class)
