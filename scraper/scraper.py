from typing import List
import requests
from bs4 import BeautifulSoup


class Scraper:
    def scrap(self) -> List[str]:
        result = requests.get('http://viti-mephi.ru/raspisanie')
        html = result.text
        soup = BeautifulSoup(html, 'lxml')

        links: List[str] = []
        link_elements = soup.select('#node-253 .file a')
        for link in link_elements:
            links.append(link.get('href'))
        return links
