from typing import (
    NoReturn,
)
from aiogram import Bot, Dispatcher

from infrastructure.ioc_container import service
from infrastructure.config import Config
from infrastructure.errors import NoReturnError
from data.serializers import JsonSerializer
from messenger_services.messenger_service import (
    MessengerService,
    PayloadSerializer,
)
from .telegram_adapter import TelegramAdapter
from .telegram_filter_adapter import TelegramFilterAdapter
from .telegram_keyboard_adapter import TelegramKeyboardAdapter


@service(to_self=True)
class TelegramService(MessengerService):
    def __init__(
            self,
            config: Config,
            keyboard_adapter: TelegramKeyboardAdapter,
            filter_adapter: TelegramFilterAdapter,
            payload_serializer: PayloadSerializer,
            json_serializer: JsonSerializer,
    ) -> None:
        bot = Bot(config.telegram_bot_token)
        self.__dispatcher = Dispatcher(bot)
        adapter = TelegramAdapter(
            bot,
            self.__dispatcher,
            keyboard_adapter,
            filter_adapter,
            payload_serializer,
            json_serializer,
        )
        super().__init__(adapter)

    async def start(self) -> NoReturn:
        await self.__dispatcher.skip_updates()
        await self.__dispatcher.start_polling()
        raise NoReturnError
