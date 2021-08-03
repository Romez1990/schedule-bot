from infrastructure.ioc_container import service
from infrastructure.env import Env
from .config import Config


@service
class ConfigImpl(Config):
    def __init__(self, env: Env) -> None:
        self.db_host = env.get_str('DB_HOST')
        self.db_name = env.get_str('DB_NAME')
        self.db_user = env.get_str('DB_USER')
        self.db_password = env.get_str('DB_PASSWORD')

        self.telegram_bot_token = env.get_str('TELEGRAM_BOT_TOKEN')
        self.vk_bot_token = env.get_str('VK_BOT_TOKEN')
