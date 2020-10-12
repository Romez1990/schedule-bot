from .user_service_interface import UserServiceInterface


class UserServiceFactoryInterface:
    def create(self, platform: str) -> UserServiceInterface:
        raise NotImplementedError
