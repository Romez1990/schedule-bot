class NothingError(Exception):
    def __init__(self) -> None:
        super().__init__('Value is nothing')
