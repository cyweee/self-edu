from app.database.connection import get_connection

from app.database.connection import get_connection

def get_full_schedule():
    """Получает всё расписание из БД"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT day, time_slot, subject, topic FROM schedule")
        return [
            {
                "day": row[0],
                "time_slot": row[1],
                "subject": row[2] or "",  # Если None - пустая строка
                "topic": row[3] or ""
            }
            for row in cursor.fetchall()
        ]
    finally:
        conn.close()

def save_schedule_item(day: str, time_slot: int, time: str, subject: str, topic: str = ""):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO schedule 
        (day, time_slot, time, subject, topic) 
        VALUES (?, ?, ?, ?, ?)
        """, (day, time_slot, time, subject, topic))
        conn.commit()
    finally:
        conn.close()

def clear_all_schedule():
    """Очищает все записи расписания"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM schedule")
        conn.commit()
    finally:
        conn.close()