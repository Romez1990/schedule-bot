from typing import (
    Callable,
)
from aiogram.dispatcher.filters import (
    Filter as TelegramFilter,
)
from aiogram.types import (
    CallbackQuery,
)

from infrastructure.ioc_container import service
from messenger_services.messenger_service import (
    Callback,
)
from messenger_services.messenger_service.filters import (
    Filter,
)


@service(to_self=True)
class TelegramFilterAdapter:
    def map_filter(self, filter: Filter, map_callback: Callable[[CallbackQuery], Callback]) -> TelegramFilter:
        return CustomFilter(filter, map_callback)


class CustomFilter(TelegramFilter):
    def __init__(self, filter: Filter, map_callback: Callable[[CallbackQuery], Callback]) -> None:
        self.__filter = filter
        self.__map_callback = map_callback

    async def check(self, query: CallbackQuery) -> bool:
        callback = self.__map_callback(query)
        return self.__filter.check(callback)
