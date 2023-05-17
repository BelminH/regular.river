import sqlite3


def add_pattern_to_category(category_name, pattern):
    # Connect to the SQLite database
    conn = sqlite3.connect("categories.db")

    # Create a cursor object
    cursor = conn.cursor()

    # Find the ID of the category
    cursor.execute(
        """
        SELECT id FROM categories WHERE name = ?
    """,
        (category_name,),
    )

    result = cursor.fetchone()
    if result is None:
        print(f"Category {category_name} not found")
        return

    category_id = result[0]

    # Insert the new pattern into the patterns table
    cursor.execute(
        """
        INSERT INTO patterns (category_id, pattern)
        VALUES (?, ?)
    """,
        (category_id, pattern),
    )

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()


# add_pattern_to_category("Food and Groceries", "NewStore") follow this format
