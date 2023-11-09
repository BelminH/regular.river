[![CodeFactor](https://www.codefactor.io/repository/github/belminh/regular.river/badge?s=6873e2cbbb77353bb89fe4c11ddb60d0ab270b58)](https://www.codefactor.io/repository/github/belminh/regular.river)
[![codecov](https://codecov.io/gh/BelminH/regular.river/branch/main/graph/badge.svg?token=6PXAPSIOCI)](https://codecov.io/gh/BelminH/regular.river)
[![Python CI](https://github.com/BelminH/regular.river/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/BelminH/regular.river/actions/workflows/build.yml)
[![Qodana](https://github.com/BelminH/regular.river/actions/workflows/qodana_code_quality.yml/badge.svg)](https://github.com/BelminH/regular.river/actions/workflows/qodana_code_quality.yml)

---

# Transaction Tally: Automated Bank Transaction Categorization

Regular River is a Python application that simplifies the management of bank transactions by automatically categorizing them into predefined groups. It processes a CSV file of transactions, applies regular expression-based rules, and tallies amounts by category, streamlining personal finance tracking.

## Quick Start

```bash
git clone git@github.com:BelminH/regular.river.git
cd regular.river
python main.py
```

## How It Works

1. **Clone the Repository**: Use Git to clone and access the codebase.
2. **Prepare Your Environment**: Ensure Python 3 is installed. If not, install it from the official Python website.
3. **Run the Script**: Execute `main.py` and input the path to your CSV file when prompted.

The script automatically classifies each transaction and presents a summary of totals for each category. Manual categorization is available for unclassified transactions.

## Features

- **Compatibility**: Currently supports Danske Bank* and Nordea formats.
- **Flexibility**: Modify regular expressions in `main.py` for other bank formats.

## Detailed Steps

1. **Installation**: Clone the repository and ensure Python 3 is set up.
2. **Usage**: Run the script, provide your CSV file, and follow the interactive prompts.
3. **Customization**: Adapt the script for different banks by editing the regex patterns.

---

- *You would need to change the position of the merchant and the amount for Danske Bank*
