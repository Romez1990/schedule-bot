from src.entities import User


class UserServiceInterface:
    async def create_if_not_exists(self, platform_id: str) -> bool:
        raise NotImplementedError

    async def find_user(self, platform_id: str) -> User:
        raise NotImplementedError
