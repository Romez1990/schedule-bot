from ..ioc_container import Module, ContainerBuilder
from .telegram_service import TelegramService
from .telegram_bot import TelegramBot
from .telegram_controller import TelegramController


class TelegramServiceModule(Module):
    def _load(self, builder: ContainerBuilder) -> None:
        builder.bind(TelegramService).to_self()
        builder.bind(TelegramBot).to_self()
        builder.bind(TelegramController).to_self()
