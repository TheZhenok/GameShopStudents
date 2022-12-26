import psycopg2
import random
from psycopg2 import Error
from werkzeug.security import generate_password_hash
from psycopg2.extensions import (
    connection as Connection,
    cursor as Cursor
)
from config import (
    USER,
    PASSWORD,
    HOST,
    PORT,
)


class Connection:
    """Class for working to DataBase"""

    def __init__(self) -> None:
        try:
            self.connection: Connection = psycopg2.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                port=PORT,
                database="flask_project"
            )
            print("[INFO] Connection is successful")
        except (Exception, Error) as e:
            print("{0} [ERROR] Connection to database is bad:".format(
                e
            ))

    def __new__(cls: type[any]) -> any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connection, cls).__new__(cls)
        return cls.instance

    # func of creating tables (game, genre, game_genre(third table with game.id, genre.id))
    def create_tables(self) -> None:
        with self.connection.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS game (
                   id SERIAL PRIMARY KEY,
                   name VARCHAR(60) NOT NULL,
                   image TEXT NOT NULL,
                   price FLOAT NOT NULL,
                   count INTEGER NOT NULL,
                   description TEXT NOT NULL,
                   rate INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS game_code(
                    id SERIAL PRIMARY KEY,
                    code TEXT NOT NULL,
                    game_id INTEGER REFERENCES game(id)
                );
                CREATE TABLE IF NOT EXISTS user_customer (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(60) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    money FLOAT DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS orders(
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES user_customer(id),
                    game_id INTEGER REFERENCES game(id)
                );
                """)
        self.connection.commit()
        print("[INFO] Tables is created")

    def adding_to_game(self,name,image,price,count,description,rate):
        with self.connection.cursor() as cur:
            cur.execute(f"""
                INSERT INTO game (name, image, price, count, description, rate) 
                VALUES ('{name}', '{image}', '{price}', '{count}', '{description}', '{rate}') RETURNING ID;
            """)
            self.connection.commit()
            game_id = cur.fetchone()
            return game_id

    #function generating game code and adding to database
    def adding_to_gamecode(self,game_id):
        generated_code = 'JDF' + str(random.randint(1000, 9999)) + 'DFSDF' + str(random.randint(100, 999))
        with self.connection.cursor() as cur:
            cur.execute(f"""
                INSERT INTO game_code (code,game_id) 
                VALUES ('{generated_code}', '{game_id}');
            """)
            self.connection.commit()

    # selecting game code from database(game_code)
    def select_code_from_game(self, game_id):
        with self.connection.cursor() as cur:
            cur.execute(f"""
                SELECT game_code.code FROM game_code WHERE game_id = '{game_id}';
            """)
            self.connection.commit()
            game_code = cur.fetchone()
            return game_code

    # functiong adding user to database
    def add_user_to_database(self, username, password, money):
        with self.connection.cursor() as cur:
            hash_password = generate_password_hash(password)
            cur.execute(f"""
                INSERT INTO user_customer (username, password, money) 
                VALUES ('{username}', '{hash_password}', '{money}');
            """)
            self.connection.commit()
    
    # function showing all users in database
    def show_user_database(self):
        with self.connection.cursor() as cur:
            cur.execute(f"""SELECT username FROM user_customer;""")
            user_check: list[tuple] = cur.fetchall()
        return user_check

    # function checking username in database
    def username_check(self, username) -> list[tuple]:
        with self.connection.cursor() as cur:
            cur.execute(f"""SELECT username FROM user_customer WHERE username='{username}';""")
            user_check: list[tuple] = cur.fetchone()
        self.connection.commit()
        return user_check

    # function showing available games to existing user
    def user_buy_game(self) -> list[tuple]:
        with self.connection.cursor() as cur:
            cur.execute(f"""SELECT id,name, price, description FROM game;""")
            user_check: list[tuple] = cur.fetchall()
        self.connection.commit()
        return user_check

    # function returns user id
    def user_return_id(self, user) -> list[tuple]:
        with self.connection.cursor() as cur:
            cur.execute(f"""SELECT id FROM user_customer WHERE username='{user}';""")
            user_id: list[tuple] = cur.fetchone()
        self.connection.commit()
        return user_id

    #insert to third column (orders)
    def insert_to_orders(self,user_id,game_id):
        with self.connection.cursor() as cur:
            cur.execute(f"""
                INSERT INTO orders (user_id, game_id) 
                VALUES ('{user_id}', '{game_id}');
            """)
            self.connection.commit()

    # select id from existed users
    def select_game(self, game):
        with self.connection.cursor() as cur:
            cur.execute(f"""
                SELECT id, name, price, count FROM game WHERE name='{game}';""")
            user_id: list[tuple] = cur.fetchone()
        self.connection.commit()
        return user_id

    # function calculating user money (user_customer)
    def buying_game(self, user, game_price, count) -> None:
        with self.connection.cursor() as cur:
            cur.execute(f"""
            BEGIN;
            UPDATE user_customer SET money = money - ({game_price} * {count})
                WHERE username = '{user}';
            SAVEPOINT my_savepoint;
            COMMIT;
            """)
        self.connection.commit()

    # checking user money in database (user_customer)
    def username_check_money(self, user):
        with self.connection.cursor() as cur:
            cur.execute(f"""SELECT money FROM user_customer WHERE username='{user}';""")
            user_check: list[tuple] = cur.fetchone()
        self.connection.commit()
        return user_check

    # function calculating count of game
    def buying_game_count(self, name, game_count) -> None:
        with self.connection.cursor() as cur:
            cur.execute(f"""
            BEGIN;
            UPDATE game SET count = count - {game_count}
                WHERE name = '{name}';
            SAVEPOINT my_savepoint;
            COMMIT;
            """)
        self.connection.commit()

    # selecting users from database except entered user_id
    def select_friend_from_id(self, user_id):
        with self.connection.cursor() as cur:
            cur.execute(f"""SELECT username from user_customer WHERE id != {user_id};""")
            user_id: list[tuple] = cur.fetchall()
        self.connection.commit()
        return user_id

    # password check in username
    def select_password_from_user(self, user):
        with self.connection.cursor() as cur:
            cur.execute(f"""SELECT password from user_customer WHERE username = '{user}';""")
            user_id: list[tuple] = cur.fetchone()
        self.connection.commit()
        return user_id