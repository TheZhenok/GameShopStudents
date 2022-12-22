# For working with database

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from decouple import config
import psycopg2

from config import (
    USERNAME,
    PASSWORD,
    HOST,
    PORT,
)


class Connection:

    _instance = None

    def __init__(self) -> None:
        self.connection = psycopg2.connect(
            user=USERNAME,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            dbname='mystat'
        )
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Connection, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def create_tables(self) -> None:
        with self.connection.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS games (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(60) UNIQUE NOT NULL,
                    image VARCHAR(70) NOT NULL,
                    price FLOAT DEFAULT(0) CHECK(price >= 0) NOT NULL,
                    count INTEGER DEFAULT(0) CHECK(count >= 0) NOT NULL,
                    description TEXT NOT NULL,
                    rate FLOAT DEFAULT(0) CHECK(rate >= 0) CHECK(rate <= 10)
                );

                CREATE TABLE IF NOT EXISTS gamecodes (
                    id SERIAL PRIMARY KEY,
                    code VARCHAR(20) NOT NULL,
                    gameid INTEGER REFERENCES games(id) NOT NULL
                );

                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(50) NOT NULL
                );

                CREATE TABLE IF NOT EXISTS user_friends (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES user(id) NOT NULL,
                    friend_id INTEGER REFERENCES user(id) NOT NULL,
                    is_access BOOLEAN DEFAULT(false)
                );

                CREATE TABLE IF NOT EXISTS orders (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES user(id) NOT NULL,
                    game_id INTEGER REFERENCES games(id) NOT NULL,
                    is_success BOOLEAN DEFAULT(false)
                );

                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES user(id) NOT NULL,
                    game_id INTEGER REFERENCES games(id) NOT NULL,
                    is_enough_money BOOLEAN DEFAULT(false),
                    already_has BOOLEAN DEFAULT(false),
                    money_spent FLOAT DEFAULT(0) NOT NULL
                );
            ''')
        self.connection.commit()

conn: Connection = Connection()
conn.create_tables()