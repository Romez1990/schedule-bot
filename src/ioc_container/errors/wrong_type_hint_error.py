from typing import (
    Any,
)


class WrongTypeHintError(Exception):
    def __init__(self, name: str, type: Any) -> None:
        super().__init__(f'parameter {name} has wrong type hint {type}')
