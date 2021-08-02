from collections.abc import (
    Collection,
)

from .parameters_error import ParametersError


class MissingTypeHintError(ParametersError):
    def __init__(self, class_type: type, parameter_names: Collection[str]) -> None:
        parameters_str = self._get_parameters(parameter_names)
        super().__init__(f'"{class_type.__name__}" type constructor has not type hints for {parameters_str}')
