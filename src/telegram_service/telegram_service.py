from ..platform_service import PlatformService
from .abstract_telegram_dispatcher import AbstractTelegramDispatcher


class TelegramService(PlatformService):
    def __init__(self, dispatcher: AbstractTelegramDispatcher):
        self.__dispatcher = dispatcher

    async def start(self) -> None:
        """
        This function return dispatcher start
        :return: None
        """
        await self.__dispatcher.start()
