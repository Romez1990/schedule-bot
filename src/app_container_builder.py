from .ioc_container import ContainerBuilder, Container
from .env import EnvModule
from .database import DatabaseModule
from .migrations import MigrationsModule
from .schedule import ScheduleModule
from .repositories import RepositoriesModule
from .bot_services import BotServicesModule
from .telegram_service import TelegramServiceModule


class AppContainerBuilder:
    def __init__(self) -> None:
        self.__container_builder = ContainerBuilder()
        self.__container_builder.register_module(EnvModule)
        self.__container_builder.register_module(DatabaseModule)
        self.__container_builder.register_module(MigrationsModule)
        self.__container_builder.register_module(ScheduleModule)
        self.__container_builder.register_module(RepositoriesModule)
        self.__container_builder.register_module(BotServicesModule)
        self.__container_builder.register_module(TelegramServiceModule)

    def build(self) -> Container:
        return self.__container_builder.build()
