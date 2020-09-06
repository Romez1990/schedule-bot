from os import getenv

import asyncio
import asyncpg

DB_HOST = 'localhost'
DB_NAME = 'schedule_bot_db'
DB_USER = getenv('DB_USER_SCHEDULE_BOT')
DB_PASS = getenv('DB_PASS_SCHEDULE_BOT')


async def connect_to_database() -> asyncpg.connection:
    connect = await asyncpg.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

    try:
        if connect:
            print('truee')
            return connect
        else:
            print('none')
            return None
    except asyncpg as ex:
        print('error')
        return f"Случилась ошибка, {ex}"


async def add_data_to_database(username: str, subscribe: bool) -> None:
    connect = await connect_to_database()
    await connect.execute('''
        INSERT INTO users(username, subscribe) VALUES($1, $2)  
    ''', username, subscribe)


asyncio.get_event_loop().run_until_complete(adding_data_to_database('Dizi', False))
