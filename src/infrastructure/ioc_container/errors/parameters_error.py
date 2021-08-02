from collections.abc import (
    Collection,
)


class ParametersError(Exception):
    def _get_parameters(self, parameter_names: Collection[str]) -> str:
        s = 's' if len(parameter_names) != 1 else ''
        parameter_names_str = '", "'.join(parameter_names)
        return f'parameter{s} "{parameter_names_str}"'
