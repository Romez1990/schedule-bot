from pytest import (
    fixture,
)

from infrastructure.ioc_container import Container


@fixture(autouse=True)
def setup() -> None:
    global container
    container = Container()


container: Container


class Service:
    pass


class ServiceImpl(Service):
    pass


def test__creates_service() -> None:
    container.bind(ServiceImpl).to(Service)

    service = container.get(Service)
    assert isinstance(service, Service)
    assert isinstance(service, ServiceImpl)

    new_service = container.get(Service)
    assert new_service is service
