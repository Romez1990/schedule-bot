from infrastructure.script import AsyncScript, script


@script
class StartScript(AsyncScript):
    async def run(self) -> None:
        print('Hello, world!')
