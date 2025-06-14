from app.database import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Создаем таблицу schedule без колонки time
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

    conn.commit()
    conn.close()