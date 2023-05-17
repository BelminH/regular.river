import sqlite3

# Create a new SQLite database (or connect to it if it already exists)
conn = sqlite3.connect("categories.db")

# Create a cursor object
cursor = conn.cursor()

# Create a new table named 'categories'
cursor.execute(
    """
    CREATE TABLE categories (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
"""
)

# Create a new table named 'patterns'
cursor.execute(
    """
    CREATE TABLE patterns (
        id INTEGER PRIMARY_KEY,
        category_id INTEGER,
        pattern TEXT NOT NULL,
        FOREIGN KEY(category_id) REFERENCES categories(id)
    )
"""
)

# Define the categories
categories = {
    "Food and Groceries": [
        "REMA",
        "BUNNPRIS",
        "COOP",
        "Meny",
        "EXTRA",
        "TooGoodToG",
        "Spar",
    ],
    "Snacks/Convenience": [
        "Integrerbar",
        "Dominos",
        "VINMONOPOLET",
        "VOITECHNOLO",
        "COCA-COLA ENTERPRISE",
        "STUD.KAFÈ",
        "FOODORA",
        "Kaffibar",
    ],
    "Entertainment": [
        "BERGEN KINO",
        "NETFLIX",
        "TWITCHINTER",
        "DISNEYPLUS",
        "VALVE",
        "NINTENDO",
        "STEAM",
    ],
    "Electronic": ["Komplett"],
    "Internett": ["internett"],
    "Clothes": ["DRESSMANN"],
    "Body care and medicine": [
        "APOTEK",
        "Farmasiet",
        "LEGESENTERET",
        "Tannhelse",
    ],
    "Transportation": [
        "Ryde Technology AS",
        "Skyss",
        "Ryde",
        "VOISCOOTERS",
    ],
    "Housing": ["VARMEREGNING", "HUSLEIE", "bo.sammen.no"],
    "Other expenses": ["TEKNA", "TILE", "SPOTIFY"],
    "Other": [],
    "Income": [],
}

# Insert the categories into the table
for category, patterns in categories.items():
    cursor.execute(
        """
        INSERT INTO categories (name)
        VALUES (?)
    """,
        (category,),
    )

    # Get the ID of the newly inserted category
    category_id = cursor.lastrowid

    # Insert the patterns into the patterns table
    for pattern in patterns:
        cursor.execute(
            """
            INSERT INTO patterns (category_id, pattern)
            VALUES (?, ?)
        """,
            (category_id, pattern),
        )

# Commit the transaction
conn.commit()

# Close the connection
conn.close()
