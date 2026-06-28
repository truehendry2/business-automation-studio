import sqlite3
from datetime import datetime

DB_NAME = "automation_studio.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS automation_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            file_name TEXT,
            tool_name TEXT,
            original_rows INTEGER,
            new_rows INTEGER,
            status TEXT,
            message TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_log(file_name, tool_name, original_rows, new_rows, status, message):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO automation_logs
        (timestamp, file_name, tool_name, original_rows, new_rows, status, message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        file_name,
        tool_name,
        original_rows,
        new_rows,
        status,
        message
    ))

    conn.commit()
    conn.close()


def get_logs():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, file_name, tool_name, original_rows, new_rows, status, message
        FROM automation_logs
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows