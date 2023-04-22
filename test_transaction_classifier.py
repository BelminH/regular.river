import pytest

from transaction_classifier import classify_transactions


@pytest.fixture
def default_dicts():

    categories = {
        "Food and Groceries": [".*REMA.*", ".*BUNNPRIS.*", ".*COOP.*", ".*Meny.*", ".*EXTRA.*", ".*TooGoodToG.*", ".*Spar.*"],
        "Snacks/Convenience": [".*Integrerbar.*", ".*Dominos.*", ".*VINMONOPOLET.*", ".*VOITECHNOLO.*",
                               ".*COCA-COLA ENTERPRISE.*", ".*STUD.KAFÈ.*", ".*FOODORA.*", ".*Kaffibar.*"],
        "Entertainment": [".*BERGEN KINO.*", ".*NETFLIX.*", ".*TWITCHINTER.*", ".*DISNEYPLUS.*", ".*VALVE.*", ".*NINTENDO.*", ".*STEAM.*"],
        "Electronic": [".*Komplett.*"],
        "Internett": [".*internett.*"],
        "Clothes": [".*DRESSMANN.*"],
        "Body care and medicine": [".*APOTEK.*", ".*Farmasiet.*", ".*LEGESENTERET.*", ".*Tannhelse.*"],
        "Transportation": [".*Ryde Technology AS.*", ".*Skyss.*", ".*Ryde.*", ".*VOISCOOTERS.*"],
        "Housing": ["VARMEREGNING.*", "HUSLEIE.*", ".*bo.sammen.no.*"],
        "Other expenses": [".*TEKNA.*", ".*TILE.*", ".*SPOTIFY.*"],
        "Other": [],
        "Income": [],
    }

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

    skip = {
        "Skip": [".*Nettbank.*", ".*Overfï¿½ring.*", ".*Regningskonto.*", ".*Overføring.*", ".*DANSKE BANK.*", ".*Akademikerne.*",
                 ".*Aksjesparekonto.*", ".*Sparekonto.*"],
    }

    return categories, totals, skip


def test_classify_transactions(default_dicts):
    categories, totals, skip = default_dicts
    transactions = [
        ("REMA 1000", 100),
        ("BUNNPRIS", 50),
        ("NETFLIX", 15),
        ("Komplett", 120),
        ("Unknown Merchant", 25),
    ]
    unknown = classify_transactions(transactions, categories, totals, skip)

    assert totals["Food and Groceries"] == 150
    assert totals["Entertainment"] == 15
    assert totals["Electronic"] == 120
    assert len(unknown) == 1
    assert unknown[0] == ("Unknown Merchant", 25)


def test_classify_transactions_no_transactions(default_dicts):
    categories, totals, skip = default_dicts
    transactions = []

    # ... (same categories, totals, and skip dictionaries as before)

    unknown = classify_transactions(transactions, categories, totals, skip)

    for total in totals.values():
        assert total == 0
    assert len(unknown) == 0


def test_classify_transactions_all_unknown(default_dicts):
    categories, totals, skip = default_dicts
    transactions = [
        ("Unknown Merchant 1", 25),
        ("Unknown Merchant 2", 35),
        ("Unknown Merchant 3", 45),
    ]

    # ... (same categories, totals, and skip dictionaries as before)

    unknown = classify_transactions(transactions, categories, totals, skip)

    for total in totals.values():
        assert total == 0
    assert len(unknown) == 3


def test_classify_transactions_all_skip(default_dicts):
    categories, totals, skip = default_dicts
    transactions = [
        ("Nettbank", 100),
        ("Overfï¿½ring", 200),
        ("Sparekonto", 300),
    ]

    # Modify the skip dictionary to have more specific patterns
    skip["Skip"].extend([".*Nettbank.*", ".*Overfï¿½ring.*", ".*Sparekonto.*"])

    unknown = classify_transactions(transactions, categories, totals, skip)

    # Print the unknown list to see if the transactions are being classified as unknown
    print("Unknown transactions:", unknown)

    # Print the totals dictionary to see which category the transactions are being classified into
    print("Totals:", totals)

    for total in totals.values():
        assert total == 0




def test_classify_transactions_mixed(default_dicts):
    categories, totals, skip = default_dicts

    transactions = [
        ("REMA 1000", 100),
        ("BUNNPRIS", 50),
        ("NETFLIX", 15),
        ("Komplett", 120),
        ("Unknown Merchant", 25),
        ("Nettbank", 100),
        ("Overfï¿½ring", 200),
        ("Sparekonto", 300),
    ]

    # ... (same categories, totals, and skip dictionaries as before)

    unknown = classify_transactions(transactions, categories, totals, skip)

    assert totals["Food and Groceries"] == 150
    assert totals["Entertainment"] == 15
    assert totals["Electronic"] == 120
    assert len(unknown) == 1
    assert unknown[0] == ("Unknown Merchant", 25)
