from pathlib import Path
from io import BytesIO

from infrastructure.script import AsyncScript, script
from schedule_services.scraper import ScheduleScraper
from schedule_services.renderer import ScheduleRenderer
from schedule_services.schedule import (
    ScheduleFilter,
    Group,
)
from infrastructure.logger import LoggerFactory


@script
class RenderMyGroupScript(AsyncScript):
    def __init__(self, schedule_scraper: ScheduleScraper, schedule_filter: ScheduleFilter, renderer: ScheduleRenderer,
                 logger_factory: LoggerFactory) -> None:
        self.schedule_scraper = schedule_scraper
        self.schedule_filter = schedule_filter
        self.renderer = renderer
        self.logger = logger_factory.create()

    async def run(self) -> None:
        schedules = await self.schedule_scraper.scrap_schedules()
        if len(schedules) == 0:
            self.logger.info('No schedule')
        else:
            schedule, *_ = schedules
            filtered_schedule = self.schedule_filter.filter(schedule, [
                Group('ИС-20-Д'),
            ])
            light_schedule = self.renderer.render(filtered_schedule, 'light')
            dark_schedule = self.renderer.render(filtered_schedule, 'dark')
            self.save(light_schedule, 'light.jpg')
            self.save(dark_schedule, 'dark.jpg')
            self.logger.info('Schedule saved')

    def save(self, image_bytes: BytesIO, filename: str) -> None:
        scripts_path = Path(__file__).parent
        with open(scripts_path / filename, 'wb') as file:
            file.write(image_bytes.read())
