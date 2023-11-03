import tempfile

from helpers.file_utils import is_valid_csv_file


def test_is_csv_file():
    # Test for an existing CSV file
    with tempfile.NamedTemporaryFile(suffix=".csv") as temp_csv:
        assert is_valid_csv_file(temp_csv.name) == True

    # Test for an existing non-CSV file
    with tempfile.NamedTemporaryFile(suffix=".txt") as temp_txt:
        assert is_valid_csv_file(temp_txt.name) == False

    # Test for a non-existing file
    assert is_valid_csv_file("non_existent.csv") == False

    # Test for an existing CSV file with upper-case extension
    with tempfile.NamedTemporaryFile(suffix=".CSV") as temp_csv_upper:
        assert is_valid_csv_file(temp_csv_upper.name) == True

    # Test for a non-file path (e.g., a directory)
    with tempfile.TemporaryDirectory() as temp_dir:
        assert is_valid_csv_file(temp_dir) == False
