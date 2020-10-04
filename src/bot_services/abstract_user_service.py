from src.entities import User


class AbstractUserService:
    async def create_if_not_exists(self, platform: str, platform_id: str) -> bool:
        raise NotImplementedError

    async def find_user(self, platform: str, platform_id: str) -> User:
        raise NotImplementedError
