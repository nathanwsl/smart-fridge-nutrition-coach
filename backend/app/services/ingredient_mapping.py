
BRITISH_TO_AMERICAN: dict[str, str] = {
    "aubergine": "eggplant",
    "courgette": "zucchini",
    "coriander": "cilantro",
    "spring onion": "green onion",
    "spring onions": "green onions",
    "prawns": "shrimp",
    "prawn": "shrimp",
    "rocket": "arugula",
    "icing sugar": "powdered sugar",
    "caster sugar": "superfine sugar",
    "double cream": "heavy cream",
    "plain flour": "all-purpose flour",
    "cornflour": "cornstarch",
    "beetroot": "beet",
    "swede": "rutabaga",
    "chickpeas": "garbanzo beans",
}


def normalize_ingredient_name(name: str) -> str:
    """
    Traduit un ingrédient UK -> US si un mapping existe, sinon renvoie
    le nom original tel quel (fallback).
    """
    cleaned = name.strip().lower()
    return BRITISH_TO_AMERICAN.get(cleaned, name)