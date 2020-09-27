from typing import (
    Type,
    Callable,
)


class BindingBuilder:
    def __init__(self, base_type: Type, callback: Callable[[Type], None]) -> None:
        self.__base_type = base_type
        self.__callback = callback

    def to(self, type: Type) -> None:
        self.__callback(type)

    def to_self(self) -> None:
        self.__callback(self.__base_type)
