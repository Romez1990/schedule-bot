class DatabaseDisconnectedError(Exception):
    def __init__(self) -> None:
        super().__init__('database is disconnected')
