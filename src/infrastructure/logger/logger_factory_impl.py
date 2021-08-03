from inspect import (
    stack,
    getmodule,
)
from typing import Optional

from infrastructure.ioc_container import service
from .logger_factory import LoggerFactory
from .logger import Logger
from .logger_impl import LoggerImpl


@service
class LoggerFactoryImpl(LoggerFactory):
    def create(self, module_name: str = None) -> Logger:
        caller_module_name = self.__get_module_name(module_name)
        return LoggerImpl(caller_module_name)

    def __get_module_name(self, module_name: Optional[str]) -> str:
        caller_module_name = self.__get_caller_module_name()
        if caller_module_name == '__main__':
            if module_name is None:
                raise RuntimeError('set module name for main module')
            return module_name
        if module_name is not None:
            raise RuntimeError('cannot set module name for nonmain module')
        return caller_module_name

    def __get_caller_module_name(self) -> str:
        stack_frame_info = stack()
        caller_frame_info = stack_frame_info[3]
        caller_frame = caller_frame_info.frame
        caller_module = getmodule(caller_frame)
        if caller_module is None:
            raise RuntimeError(f'frame "{caller_frame}" does not have module')
        return caller_module.__name__
