class FloatEnvironmentVariableError(Exception):
    def __init__(self, name: str) -> None:
        super().__init__(f'environment variable {name} must be float')
