from pytest import fixture

from .scraper import Scraper


def test_fetching(scraper: Scraper) -> None:
    schedule = scraper.fetch_schedule()


@fixture
def scraper() -> Scraper:
    return Scraper()
