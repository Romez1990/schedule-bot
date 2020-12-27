from .environment_state import EnvironmentState


class EnvironmentStateFactoryInterface:
    def create_unread_environment(self) -> EnvironmentState:
        raise NotImplementedError

    def create_read_environment(self) -> EnvironmentState:
        raise NotImplementedError
