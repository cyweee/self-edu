from app.database.connection import get_connection

def get_full_schedule():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT day, time_slot, subject, topic FROM schedule")
    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "day": row[0],
            "time_slot": row[1],
            "subject": row[2],
            "topic": row[3] or ""
        }
        for row in rows
    ]

def save_schedule_item(day: str, time_slot: int, subject: str, topic: str = ""):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT OR REPLACE INTO schedule 
        (day, time_slot, subject, topic) 
        VALUES (?, ?, ?, ?)
        """, (day, time_slot, subject, topic))
        conn.commit()
    finally:
        conn.close()

def clear_schedule():
    """Очищает все записи в расписании"""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM schedule")
        conn.commit()
    finally:
        conn.close()