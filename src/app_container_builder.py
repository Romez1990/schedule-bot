from .ioc_container import ContainerBuilder, Container
from .env import EnvModule
from .database import DatabaseModule
from .http_client import HttpModule
from .schedule import ScheduleModule
from .schedule_services import ScheduleServicesModule
from .bot_services import BotServicesModule
from .platform_services import PlatformServicesModule
from .utilities import UtilitiesModule


class AppContainerBuilder:
    def __init__(self) -> None:
        self.__container_builder = ContainerBuilder()
        self.__container_builder.register_module(EnvModule)
        self.__container_builder.register_module(DatabaseModule)
        self.__container_builder.register_module(HttpModule)
        self.__container_builder.register_module(ScheduleModule)
        self.__container_builder.register_module(ScheduleServicesModule)
        self.__container_builder.register_module(BotServicesModule)
        self.__container_builder.register_module(PlatformServicesModule)
        self.__container_builder.register_module(UtilitiesModule)

    def build(self) -> Container:
        return self.__container_builder.build()
