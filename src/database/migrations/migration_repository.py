from pathlib import Path
from importlib import import_module
from re import compile as compile_regex
from typing import (
    List,
)

from .migration_repository_interface import MigrationRepositoryInterface
from .migration import Migration


class MigrationRepository(MigrationRepositoryInterface):
    def __init__(self) -> None:
        self.__target_package = 'migrations'
        self.__current_package = '.'.join(__name__.split('.')[:-1])
        self.__module_regex = compile_regex(r'^\w+Migration$')

    def get_all(self) -> List[Migration]:
        directory = Path(__file__).parent / self.__target_package
        return [self.__get_migration(path) for path in directory.iterdir() if self.__filter_path(path)]

    def __filter_path(self, path: Path) -> bool:
        return not path.is_dir() and not path.name.startswith('_')

    def __get_migration(self, file: Path) -> Migration:
        module_name: str = file.stem
        module = import_module(f'{self.__current_package}.{self.__target_package}.{module_name}')
        elements = [element for element in dir(module)
                    if not element.startswith('_') and self.__match_migration(element)]
        if not elements:
            raise Exception(f'module {module_name} does not contain migration')
        migration_name = elements[0]
        migration = getattr(module, migration_name)
        if not issubclass(migration, Migration):
            raise Exception(f'{migration.__name__} is not a migration')
        return migration()

    def __match_migration(self, element_name: str) -> bool:
        return self.__module_regex.match(element_name) is not None
