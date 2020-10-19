from src.ioc_container import Module, Container
from .user_settings_service_interface import UserSettingsServiceInterface
from .user_settings_service import UserSettingsService


class UserSettingModule(Module):
    def _load(self, container: Container) -> None:
        container.bind(UserSettingsService).to(UserSettingsServiceInterface)
