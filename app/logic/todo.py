from app.database.connection import get_connection

def get_all_tasks():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, is_completed, priority FROM todos ORDER BY created_at")
    tasks = cursor.fetchall()
    conn.close()
    return [{
        "id": t[0],
        "task": t[1],
        "completed": bool(t[2]),
        "priority": t[3]
    } for t in tasks]

def add_task(task_text, priority=None):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO todos (task, priority) VALUES (?, ?)", (task_text, priority))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def toggle_task(task_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE todos 
        SET is_completed = NOT is_completed 
        WHERE id = ?
        """, (task_id,))
        conn.commit()
    finally:
        conn.close()

def delete_task(task_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = ?", (task_id,))
        conn.commit()
    finally:
        conn.close()
