from app.database.connection import get_connection

def get_all_links():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, url, category FROM useful_links ORDER BY title")
    links = cursor.fetchall()
    conn.close()
    return [{"id": l[0], "title": l[1], "url": l[2], "category": l[3]} for l in links]

def add_link(title, url, category):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO useful_links (title, url, category) VALUES (?, ?, ?)",
            (title, url, category)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()

def delete_link(link_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM useful_links WHERE id = ?", (link_id,))
        conn.commit()
    finally:
        conn.close()