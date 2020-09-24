from ..platform_service import PlatformService
from .telegram_dispatcher import TelegramDispatcher


class TelegramService(PlatformService):
    def __init__(self, dispatcher: TelegramDispatcher):
        self.__dispatcher = dispatcher

    def start(self) -> None:
        """
        This function return dispatcher start
        :return: None
        """
        self.__dispatcher.start()
