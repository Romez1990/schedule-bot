from inspect import (
    stack,
    getmodule,
)
from pathlib import Path
from types import (
    ModuleType,
)

from infrastructure.ioc_container import service
from .caller_module_name_retriever import CallerModuleNameRetriever


@service
class CallerModuleNameRetrieverImpl(CallerModuleNameRetriever):
    def get_caller(self, stack_offset: int = 0) -> str:
        caller_module = self.__get_caller_module(1 + stack_offset)
        caller_module_name = caller_module.__name__
        if caller_module_name == '__main__':
            script_path = Path(caller_module.__file__)
            return self.__get_script_module_name(script_path)
        return caller_module_name

    def __get_caller_module(self, stack_offset: int) -> ModuleType:
        stack_frame_info = stack()
        caller_frame_info = stack_frame_info[1 + stack_offset]
        caller_frame = caller_frame_info.frame
        caller_module = getmodule(caller_frame)
        if caller_module is None:
            raise RuntimeError(f'frame "{caller_frame}" does not have module')
        return caller_module

    def __get_script_module_name(self, script_path: Path) -> str:
        script_name = script_path.stem
        return f'script.{script_name}'
