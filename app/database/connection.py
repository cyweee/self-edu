import sqlite3
import os

DB_NAME = "self_edu.db"

def get_db_path():
    # Расположение БД в корне проекта рядом с main.py
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, DB_NAME)

def get_connection():
    return sqlite3.connect(get_db_path())
