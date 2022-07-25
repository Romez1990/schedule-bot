from typing import (
    Sequence,
)

from infrastructure.ioc_container import service
from messenger_services.messenger_service import MessengerService
from messenger_services.telegram_service import TelegramService
from messenger_services.vk_service import VkService
from .messenger_service_repository import MessengerServiceRepository


@service
class MessengerServiceRepositoryImpl(MessengerServiceRepository):
    def __init__(self,
                 telegram: TelegramService,
                 vk: VkService) -> None:
        self.__messenger_services: Sequence[MessengerService] = [
            telegram,
            vk,
        ]

    def find_all(self) -> Sequence[MessengerService]:
        return self.__messenger_services
