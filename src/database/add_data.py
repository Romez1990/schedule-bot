from asyncio import run

from .database import Database
from ..repositories import UserRepository
from ..repositories import UserSettings
from ..repositories import UserSubscribe

from .config import database_config as dc


class AddingData:
    def __init__(self):
        self.database = Database(db_host=dc.DB_HOST, db_name=dc.DB_NAME, db_pass=dc.DB_PASS, db_user=dc.DB_USER)

    async def users(self, platform: str, platform_id: str) -> None:
        """
        Connect to table  users and add dates
        :param platform:
        :param platform_id:
        :return: None
        """
        await self.database.connect()
        user_repository = UserRepository(self.database)
        await user_repository.add(platform, platform_id)

    async def subscriptions(self, user_id: int, group_name: str) -> None:
        """
        Connect to table subscriptions and add dates
        :param user_id:
        :param group_name:
        :return: None
        """
        await self.database.connect()
        user_subscriptions = UserSubscribe(self.database)
        await user_subscriptions.add(user_id, group_name)

    async def user_settings(self, id: int, theme: str) -> None:
        """
        Connect to table user_settings and add dates
        :param id:
        :param theme:
        :return:
        """
        await self.database.connect()
        user_setting = UserSettings(self.database)
        await user_setting.add(id, theme)


# add_data = AddingData()
# run(add_data.user_settings(5, 'Тёмная'))

