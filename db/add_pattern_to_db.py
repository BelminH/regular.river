import sqlite3


def add_pattern_to_db(pattern, category_id):
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT INTO patterns (category_id, pattern)
    VALUES (?, ?)
    """,
        (category_id, pattern),
    )
    conn.commit()
    conn.close()
