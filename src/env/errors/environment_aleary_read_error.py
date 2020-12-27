class EnvironmentAlreadyReadError(Exception):
    def __init__(self) -> None:
        super().__init__('environment is already read')
