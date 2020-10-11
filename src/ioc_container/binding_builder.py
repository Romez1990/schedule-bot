from typing import (
    Type,
    Callable,
)


class BindingBuilder:
    def __init__(self, type: Type, callback: Callable[[Type], None]) -> None:
        self.__type = type
        self.__callback = callback

    def to(self, base_type: Type) -> None:
        self.__callback(base_type)

    def to_self(self) -> None:
        self.__callback(self.__type)
