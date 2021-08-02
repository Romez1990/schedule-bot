class WrongTypeHintError(Exception):
    def __init__(self, parameter_name: str, parameter_type: object) -> None:
        super().__init__(f'parameter {parameter_name} has wrong type hint {parameter_type}')
