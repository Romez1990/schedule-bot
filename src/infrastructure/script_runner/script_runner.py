from asyncio import get_event_loop, set_event_loop_policy, WindowsSelectorEventLoopPolicy
from typing import (
    Type,
)

from infrastructure.ioc_container import Container
from infrastructure.paths import source_root
from .base_script import ScriptBase
from .script import Script
from .async_script import AsyncScript


class ScriptRunner:
    def __init__(self) -> None:
        self.__container = Container()

    def run(self, script_type: Type[ScriptBase]) -> None:
        self.__scan_services()
        script = self.__create_script(script_type)
        self.__run_script_base(script)

    def __scan_services(self) -> None:
        self.__container.scan_services(source_root)

    def __create_script(self, script_type: Type[ScriptBase]) -> ScriptBase:
        script = self.__container.instantiate(script_type)
        script.container = self.__container
        return script

    def __run_script_base(self, script: ScriptBase) -> None:
        if isinstance(script, Script):
            self.__run_script(script)
        elif isinstance(script, AsyncScript):
            self.__run_async_script(script)
        else:
            raise TypeError(f'script type "{type(script)}" is not supported')

    def __run_script(self, script: Script) -> None:
        script.run()

    def __run_async_script(self, script: AsyncScript) -> None:
        policy = WindowsSelectorEventLoopPolicy()
        set_event_loop_policy(policy)
        event_loop = get_event_loop()
        event_loop.run_until_complete(script.run())
