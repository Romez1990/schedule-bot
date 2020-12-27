class WrongTypeHintError(Exception):
    def __init__(self, name: str, type: any) -> None:
        super().__init__(f'parameter {name} has wrong type hint {type}')
