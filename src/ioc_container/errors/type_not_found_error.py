from typing import (
    Type,
)


class TypeNotFoundError(Exception):
    def __init__(self, type: Type) -> None:
        super().__init__(f'the requested service "{type.__name__}" has not been registered')
