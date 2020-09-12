from ..repositories import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def add(self, platform: str, platform_id: str) -> None:
        # if exist return
        # else add new user
        # add defaults settings for this user
        await self.user_repository.add(platform, platform_id)
