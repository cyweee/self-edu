from app.database import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Создаем таблицу  / schedule db
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT NOT NULL,
        time_slot INTEGER NOT NULL,
        subject TEXT,
        topic TEXT,
        UNIQUE(day, time_slot) ON CONFLICT REPLACE
    )
    """)


    # Новая таблица / todolist db
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        is_completed BOOLEAN DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()