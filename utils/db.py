import sqlite3
from contextlib import closing

database = "utils/database.db"


def start():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS provider(name TEXT, address TEXT, inn TEXT, ogrn TEXT, payment TEXT, "
            "bank TEXT, correspondent TEXT, bik TEST, phone TEXT, email TEXT, director TEXT)")
        connection.commit()


def change_provider(provider_data):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM provider")
        cursor.execute(
            "INSERT INTO provider VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                provider_data["name"], provider_data["address"], provider_data["inn"], provider_data["ogrn"],
                provider_data["payment"], provider_data["bank"], provider_data["correspondent"], provider_data["bik"],
                provider_data["phone"], provider_data["email"], provider_data["director"],))
        connection.commit()
