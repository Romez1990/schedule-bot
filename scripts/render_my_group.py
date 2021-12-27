from pathlib import Path
from io import BytesIO

from infrastructure.script import AsyncScript, script
from schedule_services.scraper import ScheduleScraper
from schedule_services.renderer import ScheduleRenderer


@script
class RenderMyGroupScript(AsyncScript):
    def __init__(self, schedule_scraper: ScheduleScraper, renderer: ScheduleRenderer) -> None:
        self.schedule_scraper = schedule_scraper
        self.renderer = renderer

    async def run(self) -> None:
        schedule, *rest = await self.schedule_scraper.scrap_schedule().get_or_raise()
        filtered_schedule = schedule.filter_groups([
            'ИС-20-Д',
        ])
        light_schedule = self.renderer.render(filtered_schedule, 'light')
        dark_schedule = self.renderer.render(filtered_schedule, 'dark')
        self.save(light_schedule, 'light.jpg')
        self.save(dark_schedule, 'dark.jpg')

    def save(self, image_bytes: BytesIO, filename: str) -> None:
        scripts_path = Path(__file__).parent
        with open(scripts_path / filename, 'wb') as file:
            file.write(image_bytes.read())
