class GetConnectionTimeoutError(Exception):
    def __init__(self, timeout: float) -> None:
        super().__init__(f'get connection take more then {timeout}s')
