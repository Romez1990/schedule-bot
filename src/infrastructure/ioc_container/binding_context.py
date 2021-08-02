from typing import (
    Optional,
    Callable,
)


class BindingContext:
    def __init__(self, callback: Callable[[Optional[type], bool], None]) -> None:
        self.__callback = callback
        self.__bound = False

    def __del__(self) -> None:
        if not self.__bound:
            raise Exception('not bound')

    def to(self, base_class: type) -> None:
        self.__bound = True
        self.__callback(base_class, False)

    def to_self(self) -> None:
        self.__bound = True
        self.__callback(None, True)
