from abc import ABCMeta

from .pool_connection import PoolConnection
from .connection import Connection


class ManageablePoolConnection(PoolConnection, Connection, metaclass=ABCMeta):
    pass
