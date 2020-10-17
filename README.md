# Schedule bot

Schedule bot is VK and Telegram bot for notifying students about their schedule changing

## Getting started
These instructions will get you a copy of the project up and running on your
machine

### Prerequisites
What things you need to have globally installed:
- Python 3.8 or higher
- Pipenv
- PostgreSQL

### Installing
Install project dependencies.
```shell script
pipenv install
```

Run database migrations.
```shell script
pipenv run migrate
```

Copy .env.example to .env. Specify server
host, client url, database and Telegram and VK bot tokens.
```shell script
cp .env.example .env
```
Or instead of .env file you can set environment variables in your system.

Run project.
```shell script
pipenv run main
```

## Built With
- [AIOHTTP](https://docs.aiohttp.org) - Asynchronous HTTP Client/Server
- [asyncpg](https://magicstack.github.io/asyncpg/) - Asynchronous PostgreSQL database client
- [AIOGram](https://docs.aiogram.dev) - Asynchronous Telegram API library
- [VKWave](https://fscdev.github.io/vkwave/) - Asynchronous VK API library
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Library for pulling data out of HTML and XML
- [Pillow](https://pillow.readthedocs.io/) - Imaging library
