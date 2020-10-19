from src.schedule_services import (
    Theme,
)
from .user import User


class UserSettings:
    def __init__(self, user: User, theme: Theme) -> None:
        self.__user = user
        self.__theme = theme

    @property
    def user(self) -> User:
        return self.__user

    @property
    def theme(self) -> Theme:
        return self.__theme
