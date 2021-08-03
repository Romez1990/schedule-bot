class PositiveIntegerEnvironmentVariableError(Exception):
    def __init__(self, var_name: str) -> None:
        super().__init__(f'environment variable "{var_name}" must be greater than zero')
