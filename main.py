import re

import check_file
import os.path
import os

re.debug = True


skip = {
    "Skip": [".*Nettbank.*", ".*Overfï¿½ring.*", ".*Regningskonto.*", ".*Overføring.*", ".*DANSKE BANK.*", ".*Akademikerne.*",
             ".*Aksjesparekonto.*", ".*Sparekonto.*"],
}


# define the categories
# ".*WORD.*" this is the format
categories = {
    "Food and Groceries": [".*REMA.*", ".*BUNNPRIS.*", ".*COOP.*", ".*Meny.*", ".*EXTRA.*", ".*TooGoodToG.*", ".*Spar.*"],
    "Snacks/Convenience": [".*Integrerbar.*", ".*Dominos.*", ".*VINMONOPOLET.*", ".*VOITECHNOLO.*",
                           ".*COCA-COLA ENTERPRISE.*", ".*STUD.KAFÈ.*", ".*FOODORA.*", ".*Kaffibar.*"],
    "Entertainment": [".*BERGEN KINO.*", ".*NETFLIX.*", ".*TWITCHINTER.*", ".*DISNEYPLUS.*", ".*VALVE.*", ".*NINTENDO.*", ".*STEAM.*"],
    "Electronic": [".*Komplett.*"],
    "Internett": [".*internett.*"],
    "Clothes": [".*DRESSMANN.*"],
    "Body care and medicine": [".*APOTEK.*", ".*Farmasiet.*", ".*LEGESENTERET.*", ".*Tannhelse.*"],
    # this is the correct format: ".*Ryde Technology AS.*"
    "Transportation": [".*Ryde Technology AS.*", ".*Skyss.*", ".*Ryde.*", ".*VOISCOOTERS.*"],
    "Housing": ["VARMEREGNING.*", "HUSLEIE.*", ".*bo.sammen.no.*"],
    "Other expenses": [".*TEKNA.*", ".*TILE.*", ".*SPOTIFY.*"],
    "Other": [],
    "Income": [],
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


def get_file_name():
    while True:
        file_path = input("Enter the file path: ")
        if not os.path.exists(file_path):
            print(f"{file_path} does not exist, try again")
        elif not check_file.is_csv_file(file_path):
            print(f"{file_path} is not a CSV file, try again")
        else:
            print(f"{file_path} is a CSV file")
            return file_path


def main(file_path):
    # read the transactions from the CSV file
    with open(file=file_path, encoding="iso-8859-1") as file:
        next(file)  # skip the header line
        for line in file:
            # split the line into columns
            columns = line.strip().split(";")
            # get the merchant and amount
            merchant = columns[3].strip()
            amount = columns[4].strip()
            amount = amount.replace('"', '')
            # Remove any periods (thousands separator)
            amount = amount.replace(".", "")
            # Replace the comma with a period (decimal separator)
            amount = amount.replace(",", ".")
            amount = float(amount)  # Convert the amount to a float

            # find the category for this transaction
            found = False
            for category, merchants in categories.items():
                for merchant_name in merchants:
                    # compile the regular expression pattern for this merchant
                    pattern = re.compile(merchant_name, flags=re.IGNORECASE)
                    if pattern.match(merchant):
                        found = True
                        # add the amount to the total for this category
                        totals[category] += amount
                        break
                if found:
                    break
            # if no category was found, check if the transaction should be skipped
            if not found:
                for skip_category, skip_merchants in skip.items():
                    for skip_merchant in skip_merchants:
                        # compile the regular expression pattern for this merchant
                        pattern = re.compile(
                            skip_merchant, flags=re.IGNORECASE)
                        if pattern.match(merchant):
                            found = True
                            print(f"Skipping '{merchant}'")
                            break
                    if found:
                        break
            # if no category or skip category was found, add the transaction to the unknown list
            if not found:
                unknown.append((merchant, amount))

    # print the totals for each category
    for category, total in totals.items():
        print(f"- {merchant}: {amount:.2f}".replace('.', ','))

    # print the unknown transactions
    print(f"\n There was({len(unknown)}) unknown transactions:")
    for merchant, amount in unknown:
        print(f"- {merchant}: {amount:.2f}")

    # ask the user where to add the unknown transactions
    if unknown:
        for merchant, amount in unknown:
            print(
                f"\nWhere do you want to add the transaction for '{merchant}' with the amount {amount}?")
            for i, category in enumerate(categories, start=1):
                print(f"{i}. {category}")
            choice = int(input("Enter the number of the category: "))
            # get the selected category
            selected_category = list(categories.keys())[choice - 1]

            # add the unknown transactions to the selected category
            categories[selected_category].append(merchant)
            totals[selected_category] += amount

    # print the updated totals
    print("Updated totals:")
    for category, total in totals.items():
        # making it easier to import to google sheets
        print(f"Total for {category}: {total:.2f}".replace('.', ','))

    
    # Delete the CSV file
    print (f"\n\nDeleting {file_path}")
    os.remove(file_path)


if __name__ == '__main__':
    file_path = get_file_name()
    main(file_path)
