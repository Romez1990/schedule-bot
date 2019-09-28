from typing import List
import requests
from bs4 import BeautifulSoup


class Scraper:
    def scrap(self) -> List[str]:
        result = requests.get('http://viti-mephi.ru/raspisanie')
        html = result.text
        soup = BeautifulSoup(html, 'lxml')

        link_elements = soup.select('#node-253 .file a')
        links: List[str] = [link.get('href') for link in link_elements]
        return links
