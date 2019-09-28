from pytest import fixture
from .scraper import Scraper


def test_parser(scraper: Scraper) -> None:
    links = scraper.scrap()
    assert links
    for link in links:
        assert link.startswith('http')
        assert link.endswith('.xlsx')


@fixture
def scraper() -> Scraper:
    return Scraper()
