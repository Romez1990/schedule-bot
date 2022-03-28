class NoReturnError(Exception):
    def __init__(self) -> None:
        super().__init__('must not call this')
