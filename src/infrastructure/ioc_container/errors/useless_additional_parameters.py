from typing import (
    Collection,
)

from .parameters_error import ParametersError


class UselessAdditionalParametersError(ParametersError):
    def __init__(self, class_type: type, parameter_names: Collection[str]) -> None:
        parameter = self._get_parameters(parameter_names)
        super().__init__(f'{parameter} is not required for creating "{class_type.__name__}"')
