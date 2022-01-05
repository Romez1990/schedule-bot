from .logger import Logger
from .caller_module_name_retriever import CallerModuleNameRetriever


class LoggerImpl(Logger):
    def __init__(self, caller_module_name_retriever: CallerModuleNameRetriever) -> None:
        call_stack = [
            'logger.init',
            'logger_factory.create',
        ]
        self.__module_name = caller_module_name_retriever.get_caller(len(call_stack))

    def error(self, data: object) -> None:
        print(f'{self.__module_name}: {data}')

    def warning(self, data: object) -> None:
        print(f'{self.__module_name}: {data}')

    def info(self, data: object) -> None:
        print(f'{self.__module_name}: {data}')

    def debug(self, data: object) -> None:
        print(f'{self.__module_name}: {data}')
