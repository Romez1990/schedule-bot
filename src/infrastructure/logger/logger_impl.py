from .logger import Logger


class LoggerImpl(Logger):
    def __init__(self, module_name: str) -> None:
        self.__module_name = module_name

    def error(self, data: object) -> None:
        print(f'{self.__module_name}: {data}')

    def warning(self, data: object) -> None:
        print(f'{self.__module_name}: {data}')

    def info(self, data: object) -> None:
        print(f'{self.__module_name}: {data}')

    def debug(self, data: object) -> None:
        print(f'{self.__module_name}: {data}')
