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
        ".*FRA.*",
        ".*TIL.*",
    ],
}

# pre configures categories that will always load into the db (if they're not already there)
# if you want to add more "steps" you would do this here and either drop categories or enter it manually
categories = {
    "Income": [],
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
    "Credit": [],
}
