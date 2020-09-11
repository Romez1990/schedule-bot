from asyncio import run

from src.database.add_data import AddingData


async def main() -> None:
    """
    Here I called databases(src/database/add_data.py) methods and I transfer there data
    :return: None
    """
    add_data = AddingData()
    await add_data.users('telegram', '123123124123')
    await add_data.user_settings(6, 'Светлая')
    await add_data.subscriptions(6, 'ЗВТ-19-8й123123')


run(main())
# ---------------------------------------------------------------------------------------------------------------------
# class AddingData:
#     def __init__(self):
#         self.database = Database(db_host=dc.DB_HOST, db_name=dc.DB_NAME, db_pass=dc.DB_PASS, db_user=dc.DB_USER)
#
#     async def users(self, platform: str, platform_id: str) -> None:
#         await self.database.connect()
#         user_repository = UserRepository(self.database)
#         await user_repository.add(platform, platform_id)
#
#     async def subscriptions(self, user_id: int, group_name: str) -> None:
#         await self.database.connect()
#         user_subscriptions = UserSubscribe(self.database)
#         await user_subscriptions.add(user_id, group_name)
#
#     async def user_settings(self, id: int, theme: str) -> None:
#         await self.database.connect()
#         user_setting = UserSettings(self.database)
#         await user_setting.add(id, theme)
#
#
# add_data = AddingData()
# run(add_data.user_settings(5, 'Тёмная'))
# ---------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------
# async def users():
#     database = Database(db_host=dc.DB_HOST, db_name=dc.DB_NAME, db_pass=dc.DB_PASS, db_user=dc.DB_USER)
#     await database.connect()
#     user_repository = UserRepository(database)
#     await user_repository.add('VK', '22888232323232')
#
#
# async def subscriptions():
#     database = Database(db_host=dc.DB_HOST, db_name=dc.DB_NAME, db_pass=dc.DB_PASS, db_user=dc.DB_USER)
#     await database.connect()
#     user_subscriptions = UserSubscribe(database)
#     await user_subscriptions.add(4, 'ЗВТ-18-999')
#
#
# async def user_settings():
#     database = Database(db_host=dc.DB_HOST, db_name=dc.DB_NAME, db_pass=dc.DB_PASS, db_user=dc.DB_USER)
#     await database.connect()
#     user_setting = UserSettings(database)
#     await user_setting.add(2, 'Белая')


# async def main():
#     database = Database(db_host=dc.DB_HOST, db_name=dc.DB_NAME, db_pass=dc.DB_PASS, db_user=dc.DB_USER)
#     await database.connect()
#     user_repository = UserRepository(database)
#     user_settings = UserSettings(database)
#     user_subscriptions = UserSubscribe(database)
#     await user_repository.add('VK', '22822222')
#     await user_repository.delete('telegram', '228')
#     await user_settings.add(1, 'Тёмная')
#     await user_subscriptions.add(1, 'ЗВТ-18-9222')
# ---------------------------------------------------------------------------------------------------------------------
