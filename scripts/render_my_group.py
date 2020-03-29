from asyncio import run
from io import BytesIO

from scraper import Scraper
from renderer import Renderer
from structures import Group


async def main() -> None:
    scraper = Scraper()
    schedule = await scraper.fetch_schedule()
    my_group = schedule.filter([
        Group('4ПрИн-5.16'),
        Group('4ПрИн-5а.16'),
    ])

    renderer = Renderer()
    light_schedule = renderer.render(my_group, 'light')
    dark_schedule = renderer.render(my_group, 'dark')

    save(light_schedule, 'light.jpg')
    save(dark_schedule, 'dark.jpg')


def save(bytes_io: BytesIO, filename: str) -> None:
    with open(filename, 'wb') as file:
        file.write(bytes_io.read())


run(main())
