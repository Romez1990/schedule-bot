from .user import User


class Message:
    def __init__(self, user: User, text: str) -> None:
        self.user = user
        self.text = text
