from app.database.connection import get_connection


# Получить всё расписание как список словарей
def get_full_schedule():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT day, time_slot, subject FROM schedule")
    rows = cursor.fetchall()
    conn.close()

    # Преобразуем в список словарей
    schedule = []
    for row in rows:
        schedule.append({
            "day": row[0],
            "time_slot": row[1],
            "subject": row[2]
        })
    return schedule


# Установить предмет для конкретного дня и пары
def set_subject(day: str, time_slot: int, subject: str):
    conn = get_connection()
    cursor = conn.cursor()

    # Проверяем — есть ли уже запись
    cursor.execute(
        "SELECT id FROM schedule WHERE day = ? AND time_slot = ?",
        (day, time_slot)
    )
    result = cursor.fetchone()

    if result:
        # Обновляем существующую запись
        cursor.execute(
            "UPDATE schedule SET subject = ? WHERE day = ? AND time_slot = ?",
            (subject, day, time_slot)
        )
    else:
        # Вставляем новую запись
        cursor.execute(
            "INSERT INTO schedule (day, time_slot, subject) VALUES (?, ?, ?)",
            (day, time_slot, subject)
        )

    conn.commit()
    conn.close()
