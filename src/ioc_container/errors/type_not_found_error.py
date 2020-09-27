from typing import (
    Type,
)


class TypeNotFoundError(Exception):
    def __init__(self, type: Type) -> None:
        super().__init__(f'The requested service "{type}" has not been registered')
        self.__type = type
