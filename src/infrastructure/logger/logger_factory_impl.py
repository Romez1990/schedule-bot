from infrastructure.ioc_container import service
from .logger_factory import LoggerFactory
from .caller_module_name_retriever import CallerModuleNameRetriever
from .logger import Logger
from .logger_impl import LoggerImpl


@service
class LoggerFactoryImpl(LoggerFactory):
    def __init__(self, caller_module_name_retriever: CallerModuleNameRetriever):
        self.__caller_module_name_retriever = caller_module_name_retriever

    def create(self) -> Logger:
        return LoggerImpl(self.__caller_module_name_retriever)
