from .ioc_container import Module, Container
from .env import EnvModule
from .database import DatabaseModule
from .http_client import HttpModule
from .schedule import ScheduleModule
from .schedule_services import ScheduleServicesModule
from .bot_services import BotServicesModule
from .platform_services import PlatformServicesModule
from .utilities import UtilitiesModule


class AppModule(Module):
    def _load(self, container: Container) -> None:
        container.register_module(EnvModule)
        container.register_module(DatabaseModule)
        container.register_module(HttpModule)
        container.register_module(ScheduleModule)
        container.register_module(ScheduleServicesModule)
        container.register_module(BotServicesModule)
        container.register_module(PlatformServicesModule)
        container.register_module(UtilitiesModule)
