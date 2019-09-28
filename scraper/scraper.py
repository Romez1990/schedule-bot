import requests
from bs4 import BeautifulSoup


class Scraper:
    def scrap(self) -> None:
        html = requests.get('http://viti-mephi.ru/raspisanie').text
        soup = BeautifulSoup(html, 'lxml')
        blok = soup.find(id="node-253")

        for file in blok.find_all('span', class_='file'):
            for link in file.find_all('a'):
                print(link.get('href'))
