import sqlite3


def init_db():
    conn = sqlite3.connect("hr_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS overrides (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_name TEXT,
            original_score REAL,
            overridden_score REAL,
            reason TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_override(candidate_name, original_score, overridden_score, reason):
    conn = sqlite3.connect("hr_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO overrides (
            candidate_name,
            original_score,
            overridden_score,
            reason
        )
        VALUES (?, ?, ?, ?)
    """, (
        candidate_name,
        original_score,
        overridden_score,
        reason
    ))

    conn.commit()
    conn.close()

def fetch_overrides():
    conn = sqlite3.connect("hr_agent.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT candidate_name, original_score, overridden_score, reason
        FROM overrides
    """)

    data = cursor.fetchall()

    conn.close()

    return data