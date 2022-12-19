# Python
from datetime import datetime
from typing import Any
# Third part
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import (
    connection as Connection,
    cursor as Cursor
)
from decouple import config


class Connection:
    def __init__(self) -> None:
        try:
            self.connection: Connection = psycopg2.connect(
                dbname=config('DBNAME', cast=str),
                host=config('HOST', cast=str),
                port=config('PORT', cast=int),
                user=config('USER', cast=str),
                password=config('PASSWORD', cast=str),
            )
            
            print(f"{datetime.now} [INFO] Connection is successfull")

        except (Exception, Error) as err:
            print(f"{datetime.now} [ERROR] Connection is bad: {err}")
    
    def __new__(cls) -> Any:
        if not hasattr(cls, 'instance'):
            cls.instance = super(Connection, cls).__new__(cls)
        
        return cls.instance
    
    def users_list(self) -> list[dict]:
        users: list[dict] = []
        try:
            with self.connection.cursor() as cur:
                cur.execute("SELECT * FROM users;")
                rows = cur.fetchall()
                for row in rows:
                    users.append({
                        'id': row[0],
                        'email': row[1],
                        'wallet': row[2]
                    })
        except Error as err:
            print(f"{datetime.now} [ERROR] Error execute <users_list> {err}")
            return {
                "status": "error",
                "users": ""
            }

        return {
            "status": "success",
            "users": users
        }

    def user(self, id: int) -> dict:
        user: dict = {}
        try:
            with self.connection.cursor() as cur:
                cur.execute("""
                    SELECT * FROM users WHERE id=%s;
                """, (id,))
                row = cur.fetchall()
                
                user['id'] = row[0],
                user['email'] = row[1]
                user['wallet'] = row[2]
        except:
            print(f"{datetime.now} [ERROR] Error execute <user>")
            return {
                "status": "error",
                "user": "",
            }

        return {
            "status": "success",
            "user": user
        }

    def user_save(self, user: dict) -> dict:
        try:
            with self.connection.cursor() as cur:
                if user['id']:
                    cur.execute("""
                        UPDATE users SET
                            email=%s,
                            wallet=%s
                        WHERE id=%s
                    """, (user['email'], user['wallet'], user['id']))
                else:
                    cur.execute("""
                        INSERT INTO users(email, wallet)
                        VALUES(%s, %s)
                        RETURNING id
                    """)
                    user['id'] = cur.fetchone() 
                
            self.connection.commit()    
        
        except:
            print(f"{datetime.now} [ERROR] Error execute <user_save>")
            return {
                "message": "error",
                "user": ""
            }

        return {
            "message": "success",
            "user": user
        }

