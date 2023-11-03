import sqlite3

from helpers.static_data import categories


class DatabaseManager:
    def __init__(self, db_path):
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def create_db(self):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL
                    )
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS patterns (
                        category_id INTEGER,
                        pattern TEXT NOT NULL,
                        FOREIGN KEY(category_id) REFERENCES categories(id)
                    )
                    """
                )
                for category, patterns in categories.items():
                    cursor.execute("INSERT INTO categories (name) VALUES (?)", (category,))
                    category_id = cursor.lastrowid
                    for pattern in patterns:
                        cursor.execute("INSERT INTO patterns (category_id, pattern) VALUES (?, ?)",
                                       (category_id, pattern))
        except sqlite3.OperationalError as e:
            print(f"Database operation error: {e}")

    def load_categories(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM categories")
            for row in cursor.fetchall():
                category_id, category_name = row
                cursor.execute("SELECT pattern FROM patterns WHERE category_id = ?", (category_id,))
                categories[category_name] = [row[0] for row in cursor.fetchall()]
        return categories

    def add_pattern_to_category(self, category_name, pattern):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
            result = cursor.fetchone()
            if result is None:
                print(f"Category {category_name} not found")
                return
            category_id = result[0]
            cursor.execute("INSERT INTO patterns (category_id, pattern) VALUES (?, ?)", (category_id, pattern))

    def add_pattern_to_db(self, pattern, category_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO patterns (category_id, pattern) VALUES (?, ?)", (category_id, pattern))


# Usage:
if __name__ == "__main__":
    db_manager = DatabaseManager("C:/Users/belmi/Documents/regular.river/db/categories.db")
    db_manager.create_db()
    categories = db_manager.load_categories()
    # db_manager.add_pattern_to_category("13", "Savings")
