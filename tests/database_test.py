import pytest
from db.database_manager import DatabaseManager


@pytest.fixture
def db_manager():
    test_db_path = 'test_database.db'
    db_manager = DatabaseManager(test_db_path)
    db_manager.create_db()
    return db_manager


def test_load_categories(db_manager):
    categories = db_manager.load_categories()
    assert isinstance(categories, dict)
    assert len(categories) > 0


def test_add_pattern_to_category(db_manager):
    # Test adding a new pattern to a category
    category_name = list(db_manager.load_categories().keys())[0]  # Use an existing category name
    new_pattern = 'unique_test_pattern'
    db_manager.add_pattern_to_category(category_name, new_pattern)

    categories = db_manager.load_categories()
    assert new_pattern in categories[category_name]


def test_update_pattern(db_manager):
    # add a pattern to update later
    category_name = list(db_manager.load_categories().keys())[0]  # use an existing category name
    pattern = 'test_pattern_for_update'
    db_manager.add_pattern_to_category(category_name, pattern)
    # get the added pattern's ID
    conn = db_manager._connect()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM patterns WHERE pattern = ?", (pattern,))
    pattern_id = cursor.fetchone()[0]

    updated_pattern = 'updated_test_pattern'
    db_manager.update_pattern(pattern_id, updated_pattern)

    cursor.execute("SELECT pattern FROM patterns WHERE id = ?", (pattern_id,))
    assert cursor.fetchone()[0] == updated_pattern
