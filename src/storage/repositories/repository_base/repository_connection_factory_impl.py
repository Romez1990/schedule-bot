from infrastructure.ioc_container import service
from storage.database import PoolConnection
from .repository_connection_factory import RepositoryConnectionFactory
from .manageable_repository_connection import ManageableRepositoryConnection
from .repository_connection_impl import RepositoryConnectionImpl


@service
class RepositoryConnectionFactoryImpl(RepositoryConnectionFactory):
    def create(self, pool_connection: PoolConnection) -> ManageableRepositoryConnection:
        return RepositoryConnectionImpl(pool_connection)
