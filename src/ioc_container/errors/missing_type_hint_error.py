from typing import (
    Type,
    List,
)


class MissingTypeHintError(Exception):
    def __init__(self, type: Type, parameters: List[str]) -> None:
        parameter_list = ', '.join(parameters)
        super().__init__(f'"{type.__name__}" type constructor has not type hints in parameters {parameter_list}')
