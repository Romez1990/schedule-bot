from ..platform_service import PlatformService


class VkService(PlatformService):
    def __init__(self, dispatcher: None) -> None:  # Change dispatcher type change to another
        self.__dispatcher = dispatcher

    async def start(self) -> None:
        await self.__dispatcher.start_polling()
