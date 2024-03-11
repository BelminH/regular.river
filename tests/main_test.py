import json
import unittest
import pytest
from unittest.mock import patch, mock_open, MagicMock
from main import (
    get_file_name,
    get_transactions,
    classify_transactions,
    delete_files,
    update_sheet,
    return_credentials,
    process_file,
)


class TestGetFileName(unittest.TestCase):
    @patch("main.rename_csv_file")
    @patch("main.is_valid_csv_file")
    @patch("main.os.access")
    @patch("main.os.path.isfile")
    @patch("main.os.path.exists")
    @patch("builtins.input")
    @patch("builtins.print")
    def test_get_file_name_success(
            self,
            mock_print,
            mock_input,
            mock_exists,
            mock_isfile,
            mock_access,
            mock_is_valid_csv,
            mock_rename_csv,
    ):
        mock_input.side_effect = ["test20200101.csv"]  # the user enters a valid file
        mock_exists.return_value = True
        mock_isfile.return_value = True
        mock_access.return_value = True
        mock_is_valid_csv.return_value = True
        mock_rename_csv.return_value = "jan2020.csv"

        result = get_file_name()

        mock_rename_csv.assert_called_once_with("test20200101.csv")
        self.assertEqual(result, "jan2020.csv")
        mock_print.assert_any_call("test20200101.csv is a CSV file")
        mock_print.assert_any_call("Staring the program...\n\n")


class TestGetTransactions(unittest.TestCase):
    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
                "Bokføringsdato;Beløp;Avsender;Mottaker;Navn;Tittel;Valuta;Betalingstype\n"
                '01.03.2021;"-100,00";6031.31.88429;;;Merchant1;NOK;Tilfedig utgift\n'
                '02.03.2021;"200,50";6031.31.88429;;;Merchant2;NOK;Tilfedig inntekt\n'
        ),
    )
    def test_get_transactions_success(self, mock_file):
        expected_transactions = [("Merchant1", -100.0), ("Merchant2", 200.5)]

        result = get_transactions("random_file.csv")

        self.assertEqual(result, expected_transactions)


@pytest.fixture
def default_dicts():
    categories = {
        "Electronic": ["Komplett"],
        "Entertainment": ["NETFLIX"],
        "Food and Groceries": ["REMA 1000", "BUNNPRIS"],
    }
    totals = {category: 0 for category in categories}
    skip = {"Skip": [".*Nettbank.*", ".*Overføring.*", ".*Sparekonto.*"]}
    return categories, totals, skip


@pytest.fixture
def setup():
    categories, totals, skip = default_dicts()
    yield categories, totals, skip


"""
 Scenarios:
        1. Standard transaction set including food, entertainment, and electronics, with one unknown merchant.
        2. An empty transaction list, expecting no changes in totals and no unknown transactions.
        3. Transactions with all merchants unknown, expecting no changes in totals and all transactions marked as unknown.
        4. Transactions that should all be skipped based on the 'Skip' patterns, expecting no changes in totals and no unknown transactions.
        5. A mixed set of transactions including recognizable, unknown, and skippable entries, testing all aspects of classification.
"""


@pytest.mark.parametrize(
    "transactions,expected_totals,expected_unknown",
    [
        (
                [
                    ("REMA 1000", 100),
                    ("BUNNPRIS", 50),
                    ("NETFLIX", 15),
                    ("Komplett", 120),
                    ("Unknown Merchant", 25),
                ],
                {"Food and Groceries": 150, "Entertainment": 15, "Electronic": 120},
                [("Unknown Merchant", 25)],
        ),
        ([], {"Food and Groceries": 0, "Entertainment": 0, "Electronic": 0}, []),
        (
                [
                    ("Unknown Merchant 1", 25),
                    ("Unknown Merchant 2", 35),
                    ("Unknown Merchant 3", 45),
                ],
                {"Food and Groceries": 0, "Entertainment": 0, "Electronic": 0},
                [
                    ("Unknown Merchant 1", 25),
                    ("Unknown Merchant 2", 35),
                    ("Unknown Merchant 3", 45),
                ],
        ),
        (
                [("Nettbank", 100), ("Overføring", 200), ("Sparekonto", 300)],
                {"Food and Groceries": 0, "Entertainment": 0, "Electronic": 0},
                [],
        ),
        (
                [
                    ("REMA 1000", 100),
                    ("BUNNPRIS", 50),
                    ("NETFLIX", 15),
                    ("Komplett", 120),
                    ("Unknown Merchant", 25),
                    ("Nettbank", 100),
                    ("Overføring", 200),
                    ("Sparekonto", 300),
                ],
                {"Food and Groceries": 150, "Entertainment": 15, "Electronic": 120},
                [("Unknown Merchant", 25)],
        ),
    ],
)
def test_classify_transactions(
        default_dicts, transactions, expected_totals, expected_unknown
):
    categories, totals, skip = default_dicts

    # Execute
    unknown = classify_transactions(transactions, categories, totals, skip)

    assert totals == expected_totals
    assert unknown == expected_unknown


@pytest.fixture
def mock_service():
    with patch("main.build") as mock_build:
        yield mock_build


# Fixture to mock the datetime
@pytest.fixture
def mock_datetime():
    with patch("main.datetime") as mock_datetime:
        mock_datetime.now.return_value.month = (
            3  # simulating as if the current month is March
        )
        yield mock_datetime


@pytest.fixture
def mock_service_account():
    with patch('main.service_account.Credentials.from_service_account_file') as mock:
        yield mock


def test_update_sheet(mock_service_account, mock_service, mock_datetime):
    with patch('main.return_credentials') as mock_credentials:
        mock_credentials.return_value = ('spreadsheet_id', 'sheet_name', 'sheet_id')

        mock_credentials_instance = MagicMock()
        mock_service_account.return_value = mock_credentials_instance

        # Set up the mock service objects
        mock_sheets_service = MagicMock()
        mock_service.return_value = mock_sheets_service
        mock_values = MagicMock()
        mock_sheets_service.spreadsheets.return_value.values.return_value = mock_values
        mock_batch_update = MagicMock()
        mock_sheets_service.spreadsheets.return_value.batchUpdate.return_value = mock_batch_update

        update_sheet({'example_total': 100.0})

        # Assertions to ensure the correct calls were made
        mock_service_account.assert_called_once_with('config/client_secret.json')
        assert mock_sheets_service.spreadsheets.call_count == 2
        mock_values.update.assert_called_once()
        mock_batch_update.execute.assert_called_once()


def test_delete_files():
    test_dir = "test_dir"
    test_files = ["file1.txt", "file2.txt"]

    with patch("main.os") as mock_os:
        # Set up a mock for os.path.join to return a fake path
        mock_os.path.join.side_effect = lambda a, b: f"{a}/{b}"

        delete_files(test_dir, test_files)

        # Assertions to check if os.remove was called correctly
        expected_calls = [
            mock_os.path.join(test_dir, file_name) for file_name in test_files
        ]
        actual_calls = [call_args[0][0] for call_args in mock_os.remove.call_args_list]
        assert (
                actual_calls == expected_calls
        ), "os.remove was not called with the expected file paths"
        assert mock_os.remove.call_count == len(
            test_files
        ), f"os.remove was expected to be called {len(test_files)} times, but was called {mock_os.remove.call_count} times"


def test_return_credentials():
    # Mock data to return
    mock_data = {
        "spreadsheet": {
            "spreadsheet_id": "test_spreadsheet_id",
            "sheet_name": "test_sheet_name",
            "sheet_id": "test_sheet_id",
        }
    }

    with patch("main.open", mock_open(read_data=json.dumps(mock_data))) as mock_file:
        with patch("main.json.load", return_value=mock_data) as mock_json:
            spreadsheet_id, sheet_name, sheet_id = return_credentials()

            mock_file.assert_called_once_with("config/spreadsheet_secret.json", "r")

            mock_json.assert_called_once()

            assert (
                    spreadsheet_id == "test_spreadsheet_id"
            ), f"Expected spreadsheet_id to be 'test_spreadsheet_id', got '{spreadsheet_id}'"
            assert (
                    sheet_name == "test_sheet_name"
            ), f"Expected sheet_name to be 'test_sheet_name', got '{sheet_name}'"
            assert (
                    sheet_id == "test_sheet_id"
            ), f"Expected sheet_id to be 'test_sheet_id', got '{sheet_id}'"
