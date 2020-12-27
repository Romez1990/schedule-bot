class EnvironmentUnreadError(Exception):
    def __init__(self) -> None:
        super().__init__('environment is unread')
