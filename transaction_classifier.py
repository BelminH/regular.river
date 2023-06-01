import os
import re

from db.add_pattern_to_db import add_pattern_to_db
from db.db_operations import load_categories
from file_utils import (
    is_valid_csv_file,
    rename_csv_file,
    get_folder_path,
    scan_folder_for_csv,
)

skip = {
    "Skip": [
        ".*Nettbank.*",
        ".*Overfï¿½ring.*",
        ".*Regningskonto.*",
        ".*Overføring.*",
        ".*DANSKE BANK.*",
        ".*Akademikerne.*",
        ".*Aksjesparekonto.*",
        ".*Sparekonto.*",
    ],
}

# create a dictionary to store the totals for each category
totals = {
    "Food and Groceries": 0,
    "Snacks/Convenience": 0,
    "Entertainment": 0,
    "Electronic": 0,
    "Internett": 0,
    "Clothes": 0,
    "Body care and medicine": 0,
    "Transportation": 0,
    "Housing": 0,
    "Other expenses": 0,
    "Other": 0,
    "Income": 0,
}

# create a list for unknown transactions
unknown = []

categories = load_categories()

debug = True


def get_file_name():
    while True:
        file_path = input("Enter the file path: ")
        if not os.path.exists(file_path):
            print(f"{file_path} does not exist, try again")
        elif not is_valid_csv_file(file_path):
            print(f"{file_path} is not a CSV file, try again")
        else:
            print(f"{file_path} is a CSV file")
            print(f"Staring the program...\n\n")
            return rename_csv_file(file_path)


def get_transactions(file_name):
    transactions = []
    with open(file=file_name, encoding="iso-8859-1") as file:
        next(file)  # skip the header line
        for line in file:
            columns = line.strip().split(";")
            merchant = columns[3].strip()
            amount = columns[4].strip()
            amount = amount.replace('"', "")
            amount = amount.replace(".", "")
            amount = amount.replace(",", ".")
            amount = float(amount)
            transactions.append((merchant, amount))
    return transactions


def classify_transactions(transactions, categories, totals, skip):
    unknown = []
    for merchant, amount in transactions:
        found = False

        # First, check the skip dictionary
        for skip_category, skip_merchants in skip.items():
            for skip_merchant in skip_merchants:
                pattern = re.compile(f".*{skip_merchant}.*", flags=re.IGNORECASE)
                if pattern.match(merchant):
                    found = True
                    break
            if found:
                break

        # If the transaction was not skipped, try to categorize it
        if not found:
            for category, merchants in categories.items():
                for merchant_name in merchants:
                    pattern = re.compile(f".*{merchant_name}.*", flags=re.IGNORECASE)
                    if pattern.match(merchant):
                        found = True
                        totals[category] += amount
                        break
                if found:
                    break

        # Add the transaction to the unknown list if it was neither skipped nor categorized
        if not found:
            unknown.append((merchant, amount))

    return unknown


def main(directory_path, csv_files):
    unknown_transactions = []  # A list to store unknown transactions from all files

    for csv_file in csv_files:
        try:
            full_path = os.path.join(directory_path, csv_file)
            print(f"\nProcessing file: {full_path}")
            transactions = get_transactions(full_path)
            unknown = classify_transactions(transactions, categories, totals, skip)

            # Store unknown transactions from current file
            for merchant, amount in unknown:
                unknown_transactions.append((csv_file, merchant, amount))
        except Exception as e:
            print(f"An error occurred while processing {csv_file}: {str(e)}")
        finally:
            print(f"Finished processing without errors on file {csv_file}")

        # print the totals for each category
        for category, total in totals.items():
            print(f"- {category}: {total:.2f}".replace(".", ","))

        # print the unknown transactions
        print(f"\n There was({len(unknown)}) unknown transactions:")
        for merchant, amount in unknown:
            print(f"- {merchant}: {amount:.2f}")

    # ask the user where to add the unknown transactions
    if unknown_transactions:
        for csv_file, merchant, amount in unknown_transactions:
            print(
                f"\nWhere do you want to add the transaction for '{merchant}' from file '{csv_file}' with the amount {amount}?"
            )
            for i, category in enumerate(categories, start=1):
                print(f"{i}. {category}")
            choice = int(input("Enter the number of the category: "))
            # get the selected category
            selected_category = list(categories.keys())[choice - 1]

            # add the unknown transactions to the selected category
            categories[selected_category].append(merchant)
            totals[selected_category] += amount

            # ask the user if they want to add the merchant to the skip list
            add_to_skip = input(
                f"Do you want to add '{merchant}' to the skip list? (y/n): "
            )
            if add_to_skip.lower() == "y":
                skip["Skip"].append(merchant)
                print(f"'{merchant}' has been added to the skip list.")

                # Ask the user if they want to add the merchant to the database
                db_name = input("What would you like to name it in the database?: ")
                category_id = choice  # The ID of the selected category
                add_pattern_to_db(db_name, category_id)

    # print the updated totals
    print(f"\n\n Updated totals:")
    for category, total in totals.items():
        # making it easier to import to google sheets
        print(f"Total for {category}: {total:.2f}".replace(".", ","))

    # Delete the CSV file
    if not debug:
        for csv_file in csv_files:
            full_path = os.path.join(directory_path, csv_file)
            print(f"\n\nDeleting {full_path}")
            os.remove(full_path)
    else:
        print(f"Not deleted, debug is turned on!")


if __name__ == "__main__":
    directory_path = get_folder_path()
    csv_files = scan_folder_for_csv(directory_path)

    # Rename all CSV files within the directory
    renamed_csv_files = []
    for csv_file in csv_files:
        full_path = os.path.join(directory_path, csv_file)
        new_file_path = rename_csv_file(full_path)
        renamed_csv_files.append(os.path.basename(new_file_path))

    # Process the renamed CSV files
    main(directory_path, renamed_csv_files)
