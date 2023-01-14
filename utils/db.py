import sqlite3
from contextlib import closing
from sqlite3 import Connection, Cursor

database = "utils/database.db"


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def start():
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS provider(name TEXT, address TEXT, inn TEXT, ogrn TEXT, "
            "bank_id INT, phone TEXT, email TEXT, director TEXT)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS banks(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, bik TEXT, payment TEXT, correspondent TEXT)")
        connection.commit()


def change_provider(provider_data):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM provider")
        cursor.execute(
            "INSERT INTO provider VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (provider_data["name"], provider_data["address"],
                                                                    provider_data["inn"], provider_data["ogrn"],
                                                                    provider_data["bank_id"], provider_data["phone"],
                                                                    provider_data["email"], provider_data["director"],))
        connection.commit()


def get_banks():
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT id, name FROM banks")
        return cursor.fetchall()

def get_bank(bank_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT * FROM banks WHERE id = ?", (bank_id,))
        return cursor.fetchone()

def add_bank(bank_data):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO banks(name, bik, payment, correspondent) VALUES(?, ?, ?, ?)", (
                bank_data["name"], bank_data["bik"], bank_data["payment"], bank_data["correspondent"],))
        connection.commit()
