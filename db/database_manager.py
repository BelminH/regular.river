import sqlite3
from datetime import datetime, timedelta
from helpers.static_data import categories


class DatabaseManager:
    def __init__(self, db_path):
        """
        Initializes the DatabaseManager with a specified database path.

        :param db_path: The path to the SQLite database file.
        """
        self.db_path = db_path

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def create_db(self):
        """
        Creates the necessary tables in the database if they do not already exist.
        Inserts initial data into the categories table.
        """
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS categories (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL UNIQUE
                    )
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS patterns (
                        id INTEGER PRIMARY KEY,
                        category_id INTEGER,
                        pattern TEXT NOT NULL,
                        created_at TEXT,
                        updated_at TEXT,
                        FOREIGN KEY(category_id) REFERENCES categories(id),
                        UNIQUE(category_id, pattern)
                    )
                    """
                )
                for category, patterns in categories.items():
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO categories (name)
                        VALUES (?)
                        """,
                        (category,),
                    )
                    category_id = cursor.execute(
                        """
                        SELECT id FROM categories WHERE name = ?
                        """,
                        (category,),
                    ).fetchone()[0]
                    for pattern in patterns:
                        cursor.execute(
                            """
                            INSERT OR IGNORE INTO patterns (category_id, pattern, created_at, updated_at)
                            VALUES (?, ?, datetime('now'), datetime('now', '+2 hours'))
                            """,
                            (category_id, pattern),
                        )
        except sqlite3.OperationalError as e:
            print(f"Database operation error: {e}")

    def add_updated_at_column(self):
        try:
            with self._connect() as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA table_info(patterns);")
                columns = [column[1] for column in cursor.fetchall()]
                if "updated_at" not in columns:
                    cursor.execute(
                        """
                        CREATE TABLE IF NOT EXISTS patterns_new (
                            id INTEGER PRIMARY KEY,
                            category_id INTEGER,
                            pattern TEXT NOT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY(category_id) REFERENCES categories(id)
                        );
                        """
                    )
                    cursor.execute(
                        """
                        INSERT INTO patterns (id, category_id, pattern)
                        SELECT id, category_id, pattern FROM patterns;
                        """
                    )
                    cursor.execute("DROP TABLE patterns;")
                    cursor.execute("ALTER TABLE patterns RENAME TO patterns;")
        except sqlite3.OperationalError as e:
            print(f"Database operation error: {e}")

    def load_categories(self):
        """
        Loads all categories and their associated patterns from the database.

        :return: A dictionary where keys are category names and values are lists of patterns.
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name FROM categories")
            for row in cursor.fetchall():
                category_id, category_name = row
                cursor.execute(
                    "SELECT pattern FROM patterns WHERE category_id = ?", (category_id,)
                )
                categories[category_name] = [row[0] for row in cursor.fetchall()]
        return categories

    def add_pattern_to_category(self, category_name, pattern):
        """
        Adds a new pattern to the database with a specified category ID.

        :param pattern: The pattern to be added.
        :param category_name: The ID of the category.
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
            result = cursor.fetchone()
            if result is None:
                print(f"Category {category_name} not found")
                return
            category_id = result[0]
            cursor.execute(
                "INSERT INTO patterns (category_id, pattern) VALUES (?, ?)",
                (category_id, pattern),
            )

    def add_pattern_to_db(self, pattern, category_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO patterns (category_id, pattern, created_at, updated_at)
                VALUES (?, ?, datetime('now'), datetime('now', '+2 hours'))
                """,
                (category_id, pattern),
            )

    def update_pattern(self, pattern_id, new_pattern):
        """
        Updates an existing pattern in the database.

        :param pattern_id: The ID of the pattern to be updated.
        :param new_pattern: The new pattern text.
        """
        with self._connect() as conn:
            cursor = conn.cursor()
            updated_at = (datetime.utcnow() + timedelta(hours=2)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            cursor.execute(
                "UPDATE patterns SET pattern = ?, updated_at = ? WHERE id = ?",
                (new_pattern, updated_at, pattern_id),
            )


if __name__ == "__main__":
    db_manager = DatabaseManager(
        "categories.db"
    )
    db_manager.create_db()
    db_manager.add_updated_at_column()  # Call this method to add the updated_at column
    categories = db_manager.load_categories()
    # db_manager.update_pattern(1, "UpdatedPattern")  # example call to update a pattern
