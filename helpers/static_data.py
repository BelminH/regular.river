__SKIP = {
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
__TOTALS = {
    "Food and Groceries": 0,
    "Snacks/Convenience": 0,
    "Entertainment": 0,
    "Electronic": 0,
    "Internet": 0,
    "Clothes": 0,
    "Body care and medicine": 0,
    "Transportation": 0,
    "Housing": 0,
    "Other expenses": 0,
    "Other": 0,
    "Savings": 0,
    "Income": 0,
}

# pre configures categories that will always load into the db (if they're not already there)
categories = {
    "Food and Groceries": [
        "REMA",
        "BUNNPRIS",
        "COOP",
        "Meny",
        "EXTRA",
        "TooGoodToG",
        "Spar",
    ],
    "Snacks/Convenience": [
        "Integrerbar",
        "Dominos",
        "VINMONOPOLET",
        "VOITECHNOLO",
        "COCA-COLA ENTERPRISE",
        "STUD.KAFÈ",
        "FOODORA",
        "Kaffibar",
    ],
    "Entertainment": [
        "BERGEN KINO",
        "NETFLIX",
        "TWITCHINTER",
        "DISNEYPLUS",
        "VALVE",
        "NINTENDO",
        "STEAM",
    ],
    "Electronic": ["Komplett"],
    "Internett": ["internett"],
    "Clothes": ["DRESSMANN"],
    "Body care and medicine": [
        "APOTEK",
        "Farmasiet",
        "LEGESENTERET",
        "Tannhelse",
    ],
    "Transportation": [
        "Ryde Technology AS",
        "Skyss",
        "Ryde",
        "VOISCOOTERS",
    ],
    "Housing": ["VARMEREGNING", "HUSLEIE", "bo.sammen.no"],
    "Other expenses": ["TEKNA", "TILE", "SPOTIFY"],
    "Other": [],
    "Savings": [],
    "Income": [],
}
