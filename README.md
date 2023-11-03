[![CodeFactor](https://www.codefactor.io/repository/github/belminh/regular.river/badge?s=6873e2cbbb77353bb89fe4c11ddb60d0ab270b58)](https://www.codefactor.io/repository/github/belminh/regular.river)
[![codecov](https://codecov.io/gh/BelminH/regular.river/branch/main/graph/badge.svg?token=6PXAPSIOCI)](https://codecov.io/gh/BelminH/regular.river)
[![Python CI](https://github.com/BelminH/regular.river/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/BelminH/regular.river/actions/workflows/build.yml)
[![Qodana](https://github.com/BelminH/regular.river/actions/workflows/qodana_code_quality.yml/badge.svg)](https://github.com/BelminH/regular.river/actions/workflows/qodana_code_quality.yml)

# Auto Bank 

Auto Bank is a Python script designed to automate the categorization of bank transactions. It reads a CSV file containing bank transactions, categorizes them based on predefined regular expressions, and displays the total amounts for each category. For transactions that don't match any existing categories, it provides an interactive interface for the user to categorize these transactions manually.

## Installation

1. Clone the repository to your local machine using the following command:
`git clone git@github.com:BelminH/regular.river.git`
2. Navigate to the cloned directory:
`python --version`
If Python 3 is not installed, please refer to the official Python documentation for installation instructions.

## Usage

To run the script, follow the steps below:

1. Run the script using Python:
`python main.py`

2. When prompted, enter the file path for the CSV file that contains the bank transactions.

The script will then categorize the transactions and display the totals for each category. If there are any unknown transactions, the script will prompt the user to manually categorize them.

## Note
Currently the tested banks are Danske Bank, however. The script can be easily modified to work with other banks by changing the regular expressions in the `main.py` file.
For now the format are as follows:
```csv
"Dato";"Kategori";"Underkategori";"Tekst";"Beløp";"Saldo";"Status";"Avstemt"
```
