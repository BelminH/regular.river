import os


def is_valid_csv_file(file_path):
    """
    Checks if the given file path points to a CSV file.

    Returns:
        - True if the file is a CSV file.
        - False otherwise.
    """
    return os.path.isfile(file_path) and file_path.lower().endswith(".csv")



