import pytest

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