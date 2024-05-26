import hashlib
from pathlib import Path
import sqlite3

PATH = Path(__file__).parent / "data.db"


class Db:
    def __init__(self, table_name: str) -> None:
        self.__table_name = table_name
        self.__con = sqlite3.connect(PATH)
        self.__cursor = self.__con.cursor()

        self.__setup_table()

    def __setup_table(self) -> None:
        self.__cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {self.__table_name} (user_name TEXT PRIMARY KEY, password TEXT)
        """)

    def add_user(self, user_name: str, password: str) -> None:
        self.__cursor.execute(
            f"""INSERT OR IGNORE INTO {self.__table_name} VALUES(?, ?)""", (user_name, password)
        )
        self.__con.commit()

    def authenticate_user(self, user_name: str, password: str) -> bool:
        all_users = self.__cursor.execute(f"""SELECT * FROM {self.__table_name}""")
        for user_name1, password1 in all_users:
            if user_name1 == user_name and password1 == password:
                return True
        return False

    def printall(self):
        with self.__con:
            self.__cursor.execute("SELECT * FROM users")
            print(self.__cursor.fetchall())


DATABASE = Db('users')

