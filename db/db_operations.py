# db_operations.py

import sqlite3


def load_categories():
    categories = {}

    # Connect to the SQLite database
    conn = sqlite3.connect("db/categories.db")

    # Create a cursor object
    cursor = conn.cursor()

    # Get all categories
    cursor.execute(
        """
        SELECT id, name FROM categories
    """
    )

    for row in cursor.fetchall():
        category_id, category_name = row

        # Get all patterns for this category
        cursor.execute(
            """
            SELECT pattern FROM patterns WHERE category_id = ?
        """,
            (category_id,),
        )

        # Add the category and its patterns to the categories dictionary
        categories[category_name] = [row[0] for row in cursor.fetchall()]

    # Close the connection
    conn.close()

    return categories
