import os
import csv


def is_valid_csv_file(file_path):
    """
    Checks if the given file path points to a CSV file.

    Returns:
        - True if the file is a CSV file.
        - False otherwise.
    """
    return os.path.isfile(file_path) and file_path.lower().endswith(".csv")


def rename_csv_file(file_path):
    """
    Renames the CSV file based on the date found in the first row of the file.

    Args:
        file_path (str): The path to the original CSV file.

    Returns:
        new_file_path (str): The path to the renamed CSV file.
    """
    with open(file_path, newline='', encoding="iso-8859-1") as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Skip the header
        row = next(reader)
        date = row[0].replace('"', '')  # Remove quotes

    # Create new file name based on the date
    month, day, year = date.split(".")
    new_file_name = f"{year}.{month}.csv"

    # Rename the file
    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
    os.rename(file_path, new_file_path)

    return new_file_path
