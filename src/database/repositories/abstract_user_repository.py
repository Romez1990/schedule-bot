from returns.maybe import Maybe

from ..entities import User


class AbstractUserRepository:
    async def save(self, user: User) -> User:
        raise NotImplementedError

    async def find(self, platform: str, platform_id: str) -> Maybe[User]:
        raise NotImplementedError
