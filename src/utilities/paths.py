from pathlib import Path

from .paths_interface import PathsInterface


class Paths(PathsInterface):
    def __init__(self) -> None:
        self.__project_path = self.__get_path()

    def __get_path(self) -> Path:
        current_directory = Path(__file__).parent
        return self.__get_path_helper(current_directory)

    def __get_path_helper(self, directory: Path) -> Path:
        pipfile = directory / 'Pipfile'
        if not pipfile.exists():
            return self.__get_path_helper(directory.parent)
        return directory

    @property
    def project(self) -> Path:
        return self.__project_path

    @property
    def assets(self) -> Path:
        return self.__project_path / 'assets'
