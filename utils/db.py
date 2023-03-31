import sqlite3
from contextlib import closing
from datetime import datetime
from sqlite3 import Connection, Cursor

from config import admin_ids

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
            "CREATE TABLE IF NOT EXISTS users(user_id INT, username TEXT, first_name TEXT, reg_time INT, fi TEXT, my_role TEXT, email TEXT, my_number TEXT, office_number TEXT, site TEXT, is_activate BOOL)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS provider(name TEXT, address TEXT, inn TEXT, kpp TEXT, ogrn TEXT, phone TEXT, email TEXT, accountant TEXT, my_role TEXT, role_parent TEXT, fio TEXT, fio_parent TEXT)")
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS banks(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, bik TEXT, payment TEXT, correspondent TEXT)")
        connection.commit()


def get_user(user_id):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return cursor.fetchone()


def add_user(user_id, username, first_name):
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?, 'Иванов Иван', 'Менеджер', 'email@gmail.com', '+7 (999) 999-99-99', '+7 (495) 463-28-33', 'site.com', ?)",
            (user_id, username, first_name, int(datetime.now().timestamp()), user_id in admin_ids))
        connection.commit()


def activate_user(user_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET is_activate = TRUE where user_id = ?", (user_id,))
        connection.commit()


def ban_user(name):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET is_activate = FALSE where fi = ?", (name,))
        connection.commit()


def change_my_info(my_info, user_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE users SET fi = ?, my_role = ?, email = ?, my_number = ?, office_number = ?, site = ? where user_id = ?",
            (my_info["fi"], my_info["role"], my_info["email"], my_info["number"], my_info["office_number"],
             my_info["site"], user_id))
        connection.commit()


def change_provider(provider_data):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM provider")
        cursor.execute(
            "INSERT INTO provider VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (provider_data["name"], provider_data["address"], provider_data["inn"], provider_data["kpp"],
             provider_data["ogrn"],
             provider_data["phone"], provider_data["email"], provider_data["accountant"], provider_data["role"],
             provider_data["role_parent"], provider_data["fio"], provider_data["fio_parent"]))
        connection.commit()


def get_provider():
    with closing(sqlite3.connect(database)) as connection:
        connection.row_factory = dict_factory
        cursor: Cursor = connection.cursor()
        cursor.execute(
            "SELECT name as provider_name, address as provider_address, inn as provider_inn, kpp as provider_kpp, ogrn as provider_ogrn, "
            "phone as provider_phone, email as provider_email, my_role as provider_role,"
            "role_parent as provider_role_parent, fio as provider_fio, fio_parent as provider_fio_parent, accountant "
            "FROM provider")
        return cursor.fetchone()


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
        cursor.execute(
            "SELECT id, name as provider_bank_name, payment as provider_payment, correspondent as provider_correspondent, bik as provider_bik FROM banks WHERE id = ?",
            (bank_id,))
        return cursor.fetchone()


def add_bank(bank_data):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO banks(name, bik, payment, correspondent) VALUES(?, ?, ?, ?)", (
                bank_data["name"], bank_data["bik"], bank_data["payment"], bank_data["correspondent"],))
        connection.commit()


def delete_bank(bank_id):
    with closing(sqlite3.connect(database)) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM banks where id = ?", (bank_id,))
        connection.commit()
