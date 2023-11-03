from main import classify_transactions


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
