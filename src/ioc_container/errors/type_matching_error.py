from typing import (
    Type,
)


class TypeMatchingError(Exception):
    def __init__(self, instance: object, type: Type) -> None:
        super().__init__(f'instance {instance} is not of type {type.__name__}')
