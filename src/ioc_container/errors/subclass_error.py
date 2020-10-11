from typing import (
    Type,
)


class SubclassError(Exception):
    def __init__(self, type: Type, base_type: Type) -> None:
        super().__init__(f'type "{type.__name__}" is not subclass of "{base_type.__name__}"')
