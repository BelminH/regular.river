import json
import os
import re
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

from db.database_manager import DatabaseManager
from helpers.file_utils import (
    is_valid_csv_file,
    rename_csv_file,
    get_folder_path,
    scan_folder_for_csv,
)
from helpers.static_data import __SKIP

db_manager = DatabaseManager("db/categories.db")
categories = db_manager.load_categories()


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
            merchant, amount = columns[5].strip(), columns[1].strip()
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

        # check the skip dictionary first
        for skip_category, skip_merchants in skip.items():
            for skip_merchant in skip_merchants:
                pattern = re.compile(f".*{skip_merchant}.*", flags=re.IGNORECASE)
                if pattern.match(merchant):
                    found = True
                    break
            if found:
                break

        # if the transaction was not skipped, try to categorize it
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

        # add the transaction to the unknown list if it was neither skipped nor categorized
        if not found:
            unmatched_transactions.append((merchant, amount))

    return unmatched_transactions


def process_file(file_path):
    print(f"\nProcessing file: {file_path}")
    transactions = get_transactions(file_path)
    totals = {
        category: 0 for category in categories
    }  # initialize a new totals dictionary
    to_be_categorized = classify_transactions(transactions, categories, totals, __SKIP)
    print(f"Totals in process_file: {totals}")

    # store unknown transactions from current file
    unknown_transactions = [
        (file_path, merchant, amount) for merchant, amount in to_be_categorized
    ]

    print("Updated totals:")
    # print_totals(totals)  # print the totals for the current file at the end
    update_sheet(totals)
    print("End of process_file function")

    return unknown_transactions, totals


def process_all_files(dir_path, file):
    all_unknown_transactions = (
        []
    )  # list to store lists of unknown transactions from all files
    all_totals = []  # list to store totals dictionaries from all files

    for i in file:
        try:
            file_path = os.path.join(dir_path, i)
            unknown_transactions, totals = process_file(
                file_path
            )  # get totals from process_file

            all_unknown_transactions.append(
                unknown_transactions
            )  # append list of unknown transactions to all_unknown_transactions
            all_totals.append(totals)  # append totals dictionary to all_totals list
        except Exception as e:
            print(f"An error occurred while processing {i}: {str(e)}")
        finally:
            print(f"Finished processing without errors on file {i}")

    return all_unknown_transactions, all_totals


def handle_unknown_transactions(unknown_transactions, totals):
    if unknown_transactions:
        for file, merchant, amount in unknown_transactions:
            print(
                f"\nWhere do you want to add the transaction for '{merchant}' from file '{file}' with the amount {amount}?"
            )
            for i, category in enumerate(categories, start=1):
                print(f"{i}. {category}")

            # validate the category choice input
            while True:
                choice_input = input("Enter the number of the category: ")
                try:
                    choice = int(choice_input)
                    if 1 <= choice <= len(categories):
                        break  # exit the while loop if a valid choice is received
                    else:
                        print(
                            f"Invalid choice, please enter a number between 1 and {len(categories)}"
                        )
                except ValueError:
                    print(f"Invalid input, please enter a number")

            # get the selected category
            selected_category = list(categories.keys())[choice - 1]

            # add the unknown transactions to the selected category
            categories[selected_category].append(merchant)
            totals[selected_category] += amount

            # ask the user if they want to add the merchant to the database
            add_to_db = str.lower(
                input(f"Do you want to add '{merchant}' to the database? (y/n): ")
            )
            if add_to_db.lower() == "y":
                db_name = input("What would you like to name it in the database?: ")
                category_id = choice  # the ID of the selected category
                db_manager.add_pattern_to_db(db_name, category_id)
                print(
                    f"'{db_name}' has been added to the database under category {selected_category}."
                )


def print_totals(totals):
    print("In print_totals function:")
    for category, total in totals.items():
        formatted_total = f"{total:.2f}".replace(".", ",")
        print(f"Total for {category}: {formatted_total}")


def return_credentials():
    # makes the credentials "global"
    json_credential = "config/spreadsheet_secret.json"
    with open(json_credential, "r") as file:
        data = json.load(file)
        spreadsheet_id = data["spreadsheet"]["spreadsheet_id"]
        sheet_name = data["spreadsheet"]["sheet_name"]
        sheet_id = data["spreadsheet"]["sheet_id"]

    return spreadsheet_id, sheet_name, sheet_id


def update_sheet(totals):
    spreadsheet_id, sheet_name, sheet_id = return_credentials()

    # Load credentials and create a service object
    credentials = service_account.Credentials.from_service_account_file(
        "config/client_secret.json"
    )
    service = build("sheets", "v4", credentials=credentials)

    # map months to columns, probably a better way to do this...
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]
    month_to_google_sheet_column = {
        month: chr(66 + i) for i, month in enumerate(months)
    }

    # find the last month
    last_month_index = (datetime.now().month - 2) % 12
    last_month = months[last_month_index]

    # prepare values for insertion
    values = [
        [f"{total:.2f}".replace(".", ",").replace("-", "")] for total in totals.values()
    ]
    range_name = f"{sheet_name}!{month_to_google_sheet_column[last_month]}2:{month_to_google_sheet_column[last_month]}15"
    body = {"values": values}

    # update the google sheet with values
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",  # needed to not break the formatting, for cell {...}
            body=body,
        )
        .execute()
    )
    print(f"{result.get('updatedCells')} cells updated. Updated month: {last_month}")

    # format the updated cells as currency, meaning we're making two requests in total
    requests = [
        {
            "repeatCell": {
                "range": {
                    "sheetId": sheet_id,
                    "startRowIndex": 1,
                    "endRowIndex": 15,
                    "startColumnIndex": ord(month_to_google_sheet_column[last_month])
                    - 65,
                    "endColumnIndex": ord(month_to_google_sheet_column[last_month])
                    - 64,
                },
                "cell": {
                    "userEnteredFormat": {
                        "numberFormat": {"type": "CURRENCY", "pattern": "#,##0.00 kr"}
                        # reformat the cells after it's been inserted
                    }
                },
                "fields": "userEnteredFormat.numberFormat",
            }
        }
    ]

    body = {"requests": requests}

    response = (
        service.spreadsheets()
        .batchUpdate(spreadsheetId=spreadsheet_id, body=body)
        .execute()
    )

    print("Response from batchUpdate:", response)

    print(f"Cells formatted as currency in month: {last_month}")


def delete_files(dir_path, files):
    for f in files:
        file_path = os.path.join(dir_path, f)
        print(f"\n\nDeleting {file_path}")
        os.remove(file_path)


def main(dir_path, files):
    debug = False  # kinda stupid, but works
    # TODO might need a rework, is a bit overcomplicated
    all_unknown_transactions, all_totals = process_all_files(dir_path, files)
    for unknown_transactions, totals in zip(all_unknown_transactions, all_totals):
        handle_unknown_transactions(unknown_transactions, totals)
        print("\nUpdated totals for file {}:".format(unknown_transactions[0][0]))
        update_sheet(totals)

    if not debug:
        delete_files(dir_path, files)
    else:
        print(f"Not deleted, debug is turned on!")


if __name__ == "__main__":
    directory_path = get_folder_path()
    csv_files = scan_folder_for_csv(directory_path)

    # rename all csv files within the directory to the format monthyear.csv
    renamed_csv_files = []
    for csv_file in csv_files:
        full_path = os.path.join(directory_path, csv_file)
        new_file_path = rename_csv_file(full_path)
        if new_file_path is not None:
            renamed_csv_files.append(os.path.basename(new_file_path))
        else:
            print("could not find a valid date in the file to use")

    # process the renamed CSV files
    main(directory_path, renamed_csv_files)
