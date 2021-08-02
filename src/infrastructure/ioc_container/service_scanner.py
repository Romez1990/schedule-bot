from __future__ import annotations
from importlib import import_module
from pathlib import Path
from typing import (
    TYPE_CHECKING,
)

from .service_decorator import services

if TYPE_CHECKING:
    from .container import Container


class ServiceScanner:
    def __init__(self, container: Container) -> None:
        self.__container = container

    def scan(self, scan_directory: Path) -> None:
        self.__import_all_modules(scan_directory)
        self.__bind_services(self.__container)

    def __import_all_modules(self, scan_directory: Path) -> None:
        self.__import_root_directory(scan_directory)

    def __import_root_directory(self, root_directory: Path) -> None:
        for fs_node in root_directory.iterdir():
            self.__import_fs_node(fs_node, fs_node.stem)

    def __import_directory(self, directory: Path, parent_package: str) -> None:
        for fs_node in directory.iterdir():
            self.__import_fs_node(fs_node, f'{parent_package}.{fs_node.stem}')

    def __import_fs_node(self, fs_node: Path, full_package_name: str) -> None:
        if fs_node.is_dir():
            self.__import_directory(fs_node, full_package_name)
        elif fs_node.suffix == '.py' and fs_node.stem != '__init__':
            import_module(full_package_name)

    def __bind_services(self, container: Container) -> None:
        for service_parameters in services:
            if service_parameters.to_self:
                container.bind(service_parameters.service).to_self()
            else:
                interface = self.__get_interface(service_parameters.service)
                container.bind(service_parameters.service).to(interface)

    def __get_interface(self, service: type) -> type:
        return service.__bases__[0]
