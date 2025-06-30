import sqlite3
import os
from app.database.path import get_db_path

DB_NAME = "self_edu.db"

def get_connection():
    db_path = get_db_path()
    print(f"Using DB path: {db_path}")  # чтобы видеть в консоли путь к базе
    return sqlite3.connect(db_path)
