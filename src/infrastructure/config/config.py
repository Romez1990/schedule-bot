from abc import ABCMeta


class Config(metaclass=ABCMeta):
    db_host: str
    db_name: str
    db_user: str
    db_password: str

    db_connection_pool_max_size: int
    db_connection_pool_timeout: float

    telegram_bot_token: str
    vk_bot_token: str

    update_checker_interval: int
    weeks_to_store_schedule_hash: int
