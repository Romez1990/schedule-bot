from psycopg2 import connect
from os import getenv

import psycopg2

DB_HOST = 'localhost'
DB_NAME = 'schedule_bot_db'
DB_USER = getenv('DB_USER_SCHEDULE_BOT')
DB_PASS = getenv('DB_PASS_SCHEDULE_BOT')

conn = connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

cur = conn.cursor()

cur.execute("INSERT INTO users (id, username, subscribe) VALUES (%s, %s, %s)",
            (1,'Kuat', True))

conn.commit()

cur.close()

conn.close()
