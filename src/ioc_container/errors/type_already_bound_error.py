from typing import (
    Type,
)


class TypeAlreadyBoundError(Exception):
    def __init__(self, base_type: Type, type: Type) -> None:
        super().__init__(f'type "{base_type.__name__}" is already bound with "{type.__name__}"')
