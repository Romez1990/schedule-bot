from __future__ import annotations
from typing import (
    TYPE_CHECKING,
    Optional,
    Iterable,
)
from pyrsistent import pvector, PVector

if TYPE_CHECKING:
    from .user_settings import UserSettings
    from .subscription import Subscription


class User:
    def __init__(self, platform: str, platform_id: str, id: int = None, settings: UserSettings = None,
                 subscriptions: Iterable[Subscription] = None) -> None:
        self.__id = id
        self.__platform = platform
        self.__platform_id = platform_id
        self.__settings = settings
        self.__subscriptions = pvector(subscriptions) if subscriptions is not None else None

    @property
    def id(self) -> Optional[int]:
        return self.__id

    @property
    def platform(self) -> str:
        return self.__platform

    @property
    def platform_id(self) -> str:
        return self.__platform_id

    @property
    def settings(self) -> Optional[UserSettings]:
        return self.__settings

    @property
    def subscriptions(self) -> Optional[PVector[Subscription]]:
        return self.__subscriptions
