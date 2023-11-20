import csv
import os
from datetime import datetime


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
    with open(file_path, newline="", encoding="iso-8859-1") as f:
        reader = csv.reader(f, delimiter=";")
        next(reader)  # skip the header
        for row in reader:
            date = row[0].replace('"', "")

    # parse the date and format the new file name
    # if the row does not have a date in, go to the next
    try:
        parsed_date = datetime.strptime(date, "%Y/%m/%d")
        new_file_name = f"{parsed_date.strftime('%b').lower()}{parsed_date.year}.csv"
        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
        os.rename(file_path, new_file_path)
        return new_file_path
    except ValueError:
        pass  # go to the next line in the file

    return None


def scan_folder_for_csv(folder_path):
    """
    Scans the specified folder for non-CSV files.

    Args:
        folder_path (str): The path to the folder to scan.

    Returns:
        csv_files (list): A list of the names of non-CSV files in the folder.
    """
    csv_files = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".csv"):
            csv_files.append(filename)

    return csv_files


def get_folder_path():
    while True:
        folder_path = input("Enter the folder path: ")
        if not os.path.exists(folder_path):
            print(f"{folder_path} does not exist, try again")
        elif not os.path.isdir(folder_path):
            print(f"{folder_path} is not a folder, try again")
        else:
            non_csv_files = scan_folder_for_csv(folder_path)
            if non_csv_files:
                print("The following CSV files were found:")
                for filename in non_csv_files:
                    print(f"- {filename}")
            return folder_path
