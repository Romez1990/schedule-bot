from typing import (
    Callable,
)
from vkbottle import (
    ABCRule,
)
from vkbottle.bot import (
    MessageEvent,
)

from infrastructure.ioc_container import service
from messenger_services.messenger_service import (
    Callback,
)
from messenger_services.messenger_service.filters import (
    Filter,
)


@service(to_self=True)
class VkFilterAdapter:
    def map_filter(self, filter: Filter, map_callback: Callable[[MessageEvent], Callback]) -> ABCRule:
        return CustomRule(filter, map_callback)


class CustomRule(ABCRule[MessageEvent]):
    def __init__(self, filter: Filter, map_callback: Callable[[MessageEvent], Callback]) -> None:
        self.__filter = filter
        self.__map_callback = map_callback

    async def check(self, event: MessageEvent) -> bool:
        callback = self.__map_callback(event)
        return self.__filter.check(callback)
