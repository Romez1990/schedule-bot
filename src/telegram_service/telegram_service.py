from ..platform_service import PlatformService
from .telegram_dispatcher import TelegramDispatcher


class TelegramService(PlatformService):
    def __init__(self, dispatcher: TelegramDispatcher):
        self.__dispatcher = dispatcher

    async def start(self) -> None:
        """
        This function return dispatcher start
        :return: None
        """
        await self.__dispatcher.start()
