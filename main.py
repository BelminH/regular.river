import os
import re

from db.database_manager import DatabaseManager

from helpers.file_utils import (
    is_valid_csv_file,
    rename_csv_file,
    get_folder_path,
    scan_folder_for_csv,
)

from helpers.static_data import __SKIP, __TOTALS

db_manager = DatabaseManager("db/categories.db")

unknown = []

categories = db_manager.load_categories()

debug = True


def get_file_name():
    while True:
        file_path = input("Enter the file path: ")
        if not os.path.exists(file_path):
            print(f"{file_path} does not exist, try again")
        elif not os.path.isfile(file_path):
            print(f"{file_path} is not a file, try again")
        elif not os.access(file_path, os.R_OK):
            print(f"You do not have read permissions for {file_path}, try again")
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


def classify_transactions(transactions, category_dict, totals, skip):
    unmatched_transactions = []
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
            for category, merchants in category_dict.items():
                for merchant_name in merchants:
                    pattern = re.compile(
                        f".*{merchant_name}.*", flags=re.IGNORECASE
                    )  # ignore everything before and after as long as it contains merchant_name
                    if pattern.match(merchant):
                        found = True
                        totals[category] += amount
                        break
                if found:
                    break

        # Add the transaction to the unknown list if it was neither skipped nor categorized
        if not found:
            unmatched_transactions.append((merchant, amount))

    return unmatched_transactions


def process_file(file_path):
    print(f"\nProcessing file: {file_path}")
    transactions = get_transactions(file_path)
    to_be_categorized = classify_transactions(
        transactions, categories, __TOTALS, __SKIP
    )

    # Store unknown transactions from current file
    unknown_transactions = [
        (file_path, merchant, amount) for merchant, amount in to_be_categorized
    ]

    return unknown_transactions


def process_all_files(dir_path, file):
    all_unknown_transactions = []  # A list to store unknown transactions from all files

    for i in file:
        try:
            file_path = os.path.join(dir_path, i)
            unknown_transactions = process_file(file_path)

            all_unknown_transactions.extend(unknown_transactions)
        except Exception as e:
            print(f"An error occurred while processing {i}: {str(e)}")
        finally:
            print(f"Finished processing without errors on file {i}")

    return all_unknown_transactions


def handle_unknown_transactions(unknown_transactions):
    if unknown_transactions:
        for file, merchant, amount in unknown_transactions:
            print(
                f"\nWhere do you want to add the transaction for '{merchant}' from file '{file}' with the amount {amount}?"
            )
            for i, category in enumerate(categories, start=1):
                print(f"{i}. {category}")

            # Validate the category choice input
            while True:
                choice_input = input("Enter the number of the category: ")
                try:
                    choice = int(choice_input)
                    if 1 <= choice <= len(categories):
                        break  # Exit the while loop if a valid choice is received
                    else:
                        print(
                            f"Invalid choice, please enter a number between 1 and {len(categories)}"
                        )
                except ValueError:
                    print(f"Invalid input, please enter a number")

            # Get the selected category
            selected_category = list(categories.keys())[choice - 1]

            # Add the unknown transactions to the selected category
            categories[selected_category].append(merchant)
            __TOTALS[selected_category] += amount

            # Ask the user if they want to add the merchant to the database
            add_to_db = input(
                f"Do you want to add '{merchant}' to the database? (y/n): "
            )
            if add_to_db.lower() == "y":
                db_name = input("What would you like to name it in the database?: ")
                category_id = choice  # The ID of the selected category
                db_manager.add_pattern_to_db(db_name, category_id)
                print(
                    f"'{db_name}' has been added to the database under category {selected_category}."
                )


# TODO replace this with google api sheets later on
def print_totals():
    print(f"\n\n Updated totals:")
    for category, total in __TOTALS.items():
        # making it easier to import to google sheets
        print(f"Total for {category}: {total:.2f}".replace(".", ","))


def delete_files(dir_path, files):
    for i in files:
        file_path = os.path.join(dir_path, i)
        print(f"\n\nDeleting {file_path}")
        os.remove(file_path)


def main(dir_path, files):
    all_unknown_transactions = process_all_files(dir_path, files)
    handle_unknown_transactions(all_unknown_transactions)
    print_totals()
    if not debug:
        delete_files(dir_path, files)
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