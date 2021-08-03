from abc import ABCMeta, abstractmethod


class Config(metaclass=ABCMeta):
    db_host: str
    db_name: str
    db_user: str
    db_password: str

    telegram_bot_token: str
    vk_bot_token: str
