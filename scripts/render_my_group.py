from asyncio import run
from pathlib import Path
from io import BytesIO

from src.ioc_container import Container
from src.app_module import AppModule
from src.schedule import (
    GroupParserInterface,
)
from src.schedule_services import (
    ScheduleScraperInterface,
    ScheduleRendererInterface,
)


async def main() -> None:
    container = Container()
    container.register_module(AppModule)

    group_parser = container.get(GroupParserInterface)
    schedule_scraper = container.get(ScheduleScraperInterface)
    renderer = container.get(ScheduleRendererInterface)

    schedule = await schedule_scraper.get_schedule()
    filtered_schedule = schedule.filter([
        group_parser.parse('ИС-20-Д').unwrap(),
    ])
    light_schedule = renderer.render(filtered_schedule, 'light')
    dark_schedule = renderer.render(filtered_schedule, 'dark')
    save(light_schedule, 'light.jpg')
    save(dark_schedule, 'dark.jpg')


def save(bytes_io: BytesIO, filename: str) -> None:
    scripts_path = Path(__file__).parent
    with open(scripts_path / filename, 'wb') as file:
        file.write(bytes_io.read())


run(main())
