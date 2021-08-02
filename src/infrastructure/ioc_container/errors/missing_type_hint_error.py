from collections.abc import (
    Collection,
)


class MissingTypeHintError(Exception):
    def __init__(self, class_type: type, parameter_names: Collection[str]) -> None:
        parameters_str = self.__get_parameters(parameter_names)
        super().__init__(f'"{class_type.__name__}" type constructor has not type hints for {parameters_str}')

    def __get_parameters(self, parameter_names: Collection[str]) -> str:
        s = 's' if len(parameter_names) != 1 else ''
        parameter_names_str = '", "'.join(parameter_names)
        return f'parameter{s} "{parameter_names_str}"'
