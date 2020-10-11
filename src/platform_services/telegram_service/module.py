from src.ioc_container import Module, Container
from .telegram_service import TelegramService
from .telegram_bot import TelegramBot
from .telegram_controller import TelegramController


class TelegramServiceModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(TelegramService).to_self()
        container.bind(TelegramBot).to_self()
        container.bind(TelegramController).to_self()
