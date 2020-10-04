from src.schedule import Group
from .user import User


class Subscription:
    def __init__(self, user: User, group: Group) -> None:
        self.__user = user
        self.__group = group

    @property
    def user(self) -> User:
        return self.__user

    @property
    def group(self) -> Group:
        return self.__group
