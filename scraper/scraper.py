from typing import List
import requests
from bs4 import BeautifulSoup


class Scraper:
    def scrap(self) -> List[str]:
        html = requests.get('http://viti-mephi.ru/raspisanie').text
        soup = BeautifulSoup(html, 'lxml')
        blok = soup.find(id="node-253")

        links: List[str] = []
        for file in blok.find_all('span', class_='file'):
            for link in file.find_all('a'):
                links.append(link.get('href'))
        return links
